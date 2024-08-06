import polars as pl
import pytest
from dfstats import _make_tables, make_stats_df, show_stats
from utils import _sample_df


@pytest.fixture
def sample_df():
    return _sample_df()


def test_make_tables(sample_df):
    result = _make_tables(sample_df)

    assert isinstance(result, dict)
    assert set(result.keys()) == {"num", "cat", "datetime", "date", "null"}

    for key, df in result.items():
        assert isinstance(df, pl.DataFrame)
        assert "Variable" in df.columns
        assert "null_count" in df.columns
        if key != "null":
            assert "min" in df.columns
            assert "max" in df.columns

    # Check specific data-frames
    num_df = result["num"]
    assert set(num_df["Variable"]) == {
        "int_col",
        "float_col",
        "bool_col",
        "int_with_missing",
        "float_col_with_mean_2",
        "float_col_with_std_2",
        "float_col_with_min_7",
        "float_col_with_max_17",
    }
    assert "mean" in num_df.columns
    assert "median" in num_df.columns
    assert "std" in num_df.columns

    cat_df = result["cat"]
    assert set(cat_df.get_column("Variable")) == {
        "str_col",
        "categorical_col",
        "enum_col",
    }
    assert "n_unique" in cat_df.columns

    datetime_df = result["datetime"]
    assert set(datetime_df.get_column("Variable")) == {"datetime_col", "datetime_col_2"}
    assert "mean" in datetime_df.columns
    assert "median" in datetime_df.columns

    date_df = result["date"]
    assert set(date_df["Variable"]) == {"date_col", "date_col_2"}


def test_print_summary(sample_df, capsys):
    pl.Config.set_fmt_str_lengths(n=10000).set_tbl_width_chars(10000)
    show_stats(sample_df)
    captured = capsys.readouterr()
    output = captured.out

    # Check if the output contains expected column names
    expected_columns = ["Missing", "Mean", "Median", "Std.", "Min", "Max"]
    for col in expected_columns:
        assert col in output, f"{col} not in output"
    assert "Var" in output

    # Check if all variable names are in the output
    for col in sample_df.columns:
        assert col in output

    # Check if the output is formatted as an ASCII markdown table
    assert "|" in output
    assert "-" in output


def test_empty_dataframe():
    with pytest.raises(ValueError) as err:
        empty_df = pl.DataFrame()
        show_stats(empty_df)
        assert "Input data frame must have rows and columns" in str(err.value)


def test_single_column_dataframe():
    single_col_df = pl.DataFrame({"test_col": range(10)})
    result = _make_tables(single_col_df)
    assert isinstance(result, dict)
    assert "num" in result
    assert "test_col" in result["num"]["Variable"]


def test_all_null_column():
    null_df = pl.DataFrame({"null_col": [None] * 10})
    result = _make_tables(null_df)
    assert isinstance(result, dict)
    assert "cat" not in result
    assert len(result) == 1
    assert "null" in result
    assert "null_col" in result["null"].get_column("Variable")
    assert (
        result["null"].filter(pl.col("Variable") == "null_col").item(0, "null_count")
        == 10
    )


def testmake_stats_df(sample_df):
    summary_table = make_stats_df(sample_df)
    col_0 = summary_table.columns[0]
    sorted_cols = sorted(sample_df.columns)
    assert sorted(summary_table.get_column(col_0)) == sorted_cols

    assert (
        summary_table.filter(pl.col(col_0).eq("float_col_with_mean_2")).item(0, "Mean")
        == "2.0"
    )
    assert (
        summary_table.filter(pl.col(col_0).eq("float_col_with_std_2")).item(0, "Std.")
        == "2.0"
    )
    assert (
        summary_table.filter(pl.col(col_0).eq("float_col_with_min_7")).item(0, "Min")
        == "7.0"
    )
    assert (
        summary_table.filter(pl.col(col_0).eq("float_col_with_max_17")).item(0, "Max")
        == "17.0"
    )

    summary_table_pandas = make_stats_df(sample_df.to_pandas())
    assert sorted(summary_table_pandas.get_column(col_0)) == sorted_cols
