# Auto-generated, do not edit directly. Run `make generate_strategy_info` to update.

import enum

from pydantic import BaseModel


class StrategyName(str, enum.Enum):
    ANT_FULL_FILE_REWRITE = "ANT_FULL_FILE_REWRITE"
    ANT_UDIFF = "ANT_UDIFF"
    ANT_SEARCH_REPLACE = "ANT_SEARCH_REPLACE"
    FUNCTION_CALLING = "FUNCTION_CALLING"
    FUNCTION_CALLING_READ_ONLY = "FUNCTION_CALLING_READ_ONLY"
    RAW_GPT = "RAW_GPT"
    READ_ONLY = "READ_ONLY"
    FULL_FILE_REWRITE = "FULL_FILE_REWRITE"
    UDIFF = "UDIFF"
    ANT_UDIFF_HUNK = "ANT_UDIFF_HUNK"


class StrategyInfo(BaseModel):
    strategy_name: StrategyName
    display_name: str
    description: str
    disabled: bool
    display_order: int


STRATEGY_INFO_LIST: list[StrategyInfo] = [
    StrategyInfo(
        strategy_name=StrategyName.ANT_FULL_FILE_REWRITE,
        display_name="Full File Rewrites",
        description="Rewrites the full file every time. Use this if your files are generally less than 300 lines.",
        disabled=False,
        display_order=0,
    ),
    StrategyInfo(
        strategy_name=StrategyName.ANT_UDIFF,
        display_name="Unified Diff (Ant)",
        description="Generates diffs to edit files",
        disabled=False,
        display_order=1,
    ),
    StrategyInfo(
        strategy_name=StrategyName.ANT_SEARCH_REPLACE,
        display_name="Search and Replace (Ant)",
        description="Replaces chunks of code with new version of code. Recommended strategy for larger more complex files.",
        disabled=False,
        display_order=2,
    ),
    StrategyInfo(
        strategy_name=StrategyName.FUNCTION_CALLING,
        display_name="Function Calling",
        description="No description",
        disabled=True,
        display_order=99,
    ),
    StrategyInfo(
        strategy_name=StrategyName.FUNCTION_CALLING_READ_ONLY,
        display_name="Function Calling (Read Only)",
        description="No description",
        disabled=True,
        display_order=99,
    ),
    StrategyInfo(
        strategy_name=StrategyName.RAW_GPT,
        display_name="Raw GPT",
        description="No description",
        disabled=True,
        display_order=99,
    ),
    StrategyInfo(
        strategy_name=StrategyName.READ_ONLY,
        display_name="Read Only",
        description="No description",
        disabled=True,
        display_order=99,
    ),
    StrategyInfo(
        strategy_name=StrategyName.FULL_FILE_REWRITE,
        display_name="Full File Rewrites",
        description="Rewrites the full file every time. Use this if your files are generally less than 300 lines.",
        disabled=True,
        display_order=99,
    ),
    StrategyInfo(
        strategy_name=StrategyName.UDIFF,
        display_name="Unified Diff",
        description="Generates diffs to edit files",
        disabled=True,
        display_order=99,
    ),
    StrategyInfo(
        strategy_name=StrategyName.ANT_UDIFF_HUNK,
        display_name="Unified Diff (Hunk)",
        description="Generates diffs to edit files",
        disabled=True,
        display_order=99,
    ),
]


ENABLED_STRATEGY_INFO_LIST: list[StrategyInfo] = [
    StrategyInfo(
        strategy_name=StrategyName.ANT_FULL_FILE_REWRITE,
        display_name="Full File Rewrites",
        description="Rewrites the full file every time. Use this if your files are generally less than 300 lines.",
        disabled=False,
        display_order=0,
    ),
    StrategyInfo(
        strategy_name=StrategyName.ANT_UDIFF,
        display_name="Unified Diff (Ant)",
        description="Generates diffs to edit files",
        disabled=False,
        display_order=1,
    ),
    StrategyInfo(
        strategy_name=StrategyName.ANT_SEARCH_REPLACE,
        display_name="Search and Replace (Ant)",
        description="Replaces chunks of code with new version of code. Recommended strategy for larger more complex files.",
        disabled=False,
        display_order=2,
    ),
]
