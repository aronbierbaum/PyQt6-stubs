"""AnnotationFixer that will fix annotations on class methods."""
from __future__ import annotations

from typing import Dict, List, Optional, Sequence, TypeVar, Union, cast

from libcst import (
    Annotation,
    Assign,
    Attribute,
    BaseSmallStatement,
    BaseStatement,
    ClassDef,
    Comment,
    CSTTransformer,
    Decorator,
    FlattenSentinel,
    FunctionDef,
    ImportAlias,
    ImportFrom,
    Module,
    Name,
    Param,
    RemovalSentinel,
    SimpleStatementLine,
    SimpleStatementSuite,
    parse_expression,
    parse_statement,
)
from libcst.metadata import PositionProvider

from fixes.annotation_fixes import (
    ANNOTATION_FIXES,
    AddAnnotationFix,
    AddImportFix,
    AnnotationFix,
    CommentFix,
    FixParameter,
    RemoveFix,
    RemoveOverloadDecoratorFix,
)


class AnnotationFixer(  # pylint: disable=too-many-instance-attributes
    CSTTransformer
):
    """AnnotationFixer that will fix annotations on class methods."""

    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(
        self,
        mod_name: str,
        fixes: List[
            CommentFix | RemoveFix | RemoveOverloadDecoratorFix | AddImportFix
        ],
        last_class_method: Dict[str, FunctionDef],
    ):
        super().__init__()

        # ClassDef and FunctionDef visit stack
        self._last_class: List[ClassDef] = []
        self._last_function: List[FunctionDef] = []

        # Fixes that will be applied for the current module.
        self._fixes: List[AnnotationFix | AddAnnotationFix] = [
            fix for fix in ANNOTATION_FIXES if fix.module_name == mod_name
        ]

        # Custom type definitons to be inserted after PYQT_SLOT/PYQT_SIGNAL
        self._type_defs = set(
            fix.custom_type
            for fix in self._fixes
            if isinstance(fix, AnnotationFix) and fix.custom_type
        )
        self._insert_type_defs = False

        # Generated fixes (i.e. from mypy)
        self._generated_fixes = [
            fix for fix in fixes if not isinstance(fix, AddImportFix)
        ]
        try:
            self._add_import_fix: Optional[AddImportFix] = [
                fix for fix in fixes if isinstance(fix, AddImportFix)
            ][0]
        except IndexError:
            self._add_import_fix = None

        # Node after which the missing imports from PyQt6 will be appended
        self._import_alias_node: ImportAlias | None = None

        # Holds the last method for every class:
        self._last_class_method = last_class_method

    @property
    def class_name(self) -> str | None:
        """Return the name of the current class."""
        try:
            return self._last_class[-1].name.value
        except IndexError:
            return None

    @property
    def function_name(self) -> str | None:
        """Return the name of the current function."""
        try:
            return self._last_function[-1].name.value
        except IndexError:
            return None

    def visit_ImportFrom(self, node: ImportFrom) -> bool | None:
        if cast(Attribute, node.module).value == "PyQt6" and any(
            isinstance(fix, AddImportFix) for fix in self._generated_fixes
        ):
            # Remember the last ImportAlias node after which we will add the
            # missing imports.
            try:
                self._import_alias_node = cast(
                    Sequence[ImportAlias], node.names
                )[-1]
            except IndexError:
                # in case it's a ImportStar
                return False
            return True
        return False

    def leave_ImportAlias(
        self, original_node: ImportAlias, updated_node: ImportAlias
    ) -> Union["ImportAlias", FlattenSentinel["ImportAlias"], RemovalSentinel]:
        if self._import_alias_node and self._add_import_fix:
            exprs = [
                cast(Name, parse_expression(missing_import))
                for missing_import in self._add_import_fix.missing_imports
            ]
            new_aliases = [ImportAlias(expr) for expr in exprs]
            self._add_import_fix = None
            self._import_alias_node = None
            return FlattenSentinel([original_node] + new_aliases)
        return original_node

    def leave_Assign(
        self, original_node: Assign, updated_node: Assign
    ) -> Union[
        BaseSmallStatement,
        FlattenSentinel[BaseSmallStatement],
        RemovalSentinel,
    ]:
        name = original_node.targets[0].target.value  # type: ignore
        if name == "PYQT_SLOT":
            self._insert_type_defs = True
        return original_node

    def leave_SimpleStatementLine(
        self,
        original_node: SimpleStatementLine,
        updated_node: SimpleStatementLine,
    ) -> BaseStatement | FlattenSentinel[BaseStatement] | RemovalSentinel:
        if self._insert_type_defs and self._type_defs:
            type_defs = list(map(parse_statement, self._type_defs))
            self._insert_type_defs = False
            return FlattenSentinel([updated_node, *type_defs])
        return updated_node

    def visit_ClassDef(self, node: ClassDef) -> bool:
        """Put a class on top of the stack when visiting."""
        self._last_class.append(node)
        # Visit every class in case there's a class in a class.
        return True

    def visit_FunctionDef(self, node: FunctionDef) -> bool:
        self._last_function.append(node)
        for fix in self._generated_fixes:
            if any(fix.node == decorator for decorator in node.decorators):
                print(
                    f"Visiting function {self.class_name}.{self.function_name} to fix Decorator"
                )
                return True
        return False

    def visit_Decorator(self, node: "Decorator") -> bool | None:
        return False

    def leave_Decorator(
        self, original_node: Decorator, updated_node: Decorator
    ) -> Union[Decorator, FlattenSentinel[Decorator], RemovalSentinel]:
        """Some mypy fixes must be applied to the decorator."""
        mypy_fix = self._get_mypy_fix(original_node)
        if mypy_fix:
            if isinstance(mypy_fix, CommentFix):
                return self._apply_comment_fix(mypy_fix, updated_node)
            if isinstance(mypy_fix, RemoveOverloadDecoratorFix):
                print(
                    f"Removing obsolete decorator on {self.class_name}.{self.function_name}"
                )
                self._generated_fixes.remove(mypy_fix)
                return RemovalSentinel.REMOVE
        return original_node

    def leave_FunctionDef(  # pylint: disable=too-many-branches
        self, original_node: FunctionDef, updated_node: FunctionDef
    ) -> Union[BaseStatement, FlattenSentinel[BaseStatement], RemovalSentinel]:
        """Remove a function from the stack and return the updated node."""
        if self.class_name is None:
            # We need a class to operate, currently.
            self._last_function.pop()
            return updated_node

        # Check if we can fix the function.
        function_fix = self._get_fix()
        if function_fix:
            # Check every parameter and find the appropriate one to fix in the
            # source code.
            for param in function_fix.params:
                for original_param in updated_node.params.params:
                    if original_param.name.value == "self":
                        # Can we fix self? ;)
                        continue
                    # Fix the parameter
                    if original_param.name.value == param.name:
                        updated_node = self._fix_annotation(
                            original_param, param, updated_node
                        )
                if param.name.startswith("*"):
                    star_arg = updated_node.params.star_arg
                    updated_node = self._fix_annotation(
                        cast(Param, star_arg), param, updated_node
                    )
            # Remove the fix from the class.
            self._fixes.remove(function_fix)
            self._last_function.pop()
            return updated_node

        mypy_fix = self._get_mypy_fix(original_node)
        if mypy_fix:
            # If we have two fixes, this might have unforeseen consequences.
            assert not function_fix
            if isinstance(mypy_fix, CommentFix):
                return_value: BaseStatement | RemovalSentinel = (
                    self._apply_comment_fix(mypy_fix, updated_node)
                )
            elif isinstance(mypy_fix, RemoveFix):
                print(
                    f"Fixing method by removing it: {self.class_name}.{original_node.name.value}"
                )
                assert original_node == mypy_fix.node
                return_value = RemovalSentinel.REMOVE
                self._generated_fixes.remove(mypy_fix)
            self._last_function.pop()
            return return_value

        if self._last_class_method[self.class_name] == original_node:
            for fix in self._fixes:
                if (
                    isinstance(fix, AddAnnotationFix)
                    and self.class_name == fix.class_name
                ):
                    statements = [
                        parse_statement(annotation)
                        for annotation in fix.annotations
                    ]
                    self._fixes.remove(fix)
                    self._last_function.pop()
                    return FlattenSentinel(
                        [original_node] + cast(List[FunctionDef], statements)
                    )

        self._last_function.pop()
        return updated_node

    def _fix_annotation(
        self,
        original_param: Param,
        param: FixParameter,
        updated_node: FunctionDef,
    ) -> FunctionDef:
        """Fix the annotation of the given parameter of the FunctionDef."""
        print(
            f"Changing annotation of "
            f"{self.function_name}:{original_param.name.value}"
            f" to {param.annotation}"
        )
        expr = parse_expression(param.annotation)
        anno = Annotation(annotation=expr)
        updated_node = updated_node.with_deep_changes(
            original_param, annotation=anno
        )
        return updated_node

    def leave_ClassDef(
        self, original_node: ClassDef, updated_node: ClassDef
    ) -> BaseStatement | FlattenSentinel[BaseStatement] | RemovalSentinel:
        """Remove a class from the stack and return the updated node."""
        self._last_class.pop()
        return updated_node

    def leave_Module(
        self, original_node: Module, updated_node: Module
    ) -> Module:
        """Check if all fixes were applied before leaving the module."""
        for fix in self._fixes:
            print(f"ERROR: Fix was not applied: {fix}")
        for mypy_fix in self._generated_fixes:
            print(f"ERROR: Fix was not applied: {mypy_fix}")
        return updated_node

    def _get_fix(self) -> AnnotationFix | None:
        """Return the AnnotationFix for the current method if available."""
        for fix in self._fixes:
            if (
                isinstance(fix, AnnotationFix)
                and fix.class_name == self.class_name
                and fix.method_name == self.function_name
            ):
                child_count = len(self._last_function[-1].params.children)
                if (fix.static and child_count != len(fix.params)) or (
                    not fix.static and child_count - 1 != len(fix.params)
                ):
                    # If the number of Parameters does not match the number of
                    # Parameters to fix, we return.
                    return None

                for param in self._last_function[-1].params.params:
                    if param.name.value == "self":
                        # ignore self params
                        continue
                    if not any(
                        fix_param.name == param.name.value
                        for fix_param in fix.params
                    ):
                        print(f"Fix does not match due to param: {param.name}")
                        return None

                # Check if the function def includes a star parameter and if
                # it matches one of our fix arguments.
                star_arg = self._last_function[-1].params.star_arg
                if (
                    star_arg
                    and isinstance(star_arg, Param)
                    and not any(
                        fix_param.name == f"*{star_arg.name.value}"
                        for fix_param in fix.params
                    )
                ):
                    print(
                        f"Star argument is not matched: *{star_arg.name.value}"
                    )
                    return None

                print(f"Found fix to apply: {fix}")
                return fix
        return None

    def _get_mypy_fix(
        self, node: FunctionDef | Decorator
    ) -> CommentFix | RemoveFix | RemoveOverloadDecoratorFix | None:
        """Return a MypyFix for the given line number if available."""
        for fix in self._generated_fixes:
            if fix.node == node:
                return fix
        return None

    NodeT = TypeVar("NodeT", FunctionDef, Decorator)

    def _apply_comment_fix(
        self, fix: CommentFix, updated_node: NodeT
    ) -> NodeT:
        """Apply the given MypyFix and return an updated node."""
        if isinstance(fix, CommentFix):
            print("Fixing node by adding # type: ignore[override]")
            comment = Comment(fix.comment)
            if isinstance(updated_node, Decorator):
                change_node = updated_node.trailing_whitespace
            else:
                change_node = cast(
                    SimpleStatementSuite, updated_node.body
                ).trailing_whitespace
            updated_node = updated_node.with_deep_changes(
                change_node, comment=comment
            )
            self._generated_fixes.remove(fix)
            return updated_node
        raise ValueError(f"Don't know what to do with {fix}")
