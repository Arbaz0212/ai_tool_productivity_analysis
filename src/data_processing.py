import pandas as pd


def load_data(path):
    df = pd.read_csv(path)
    return df


def compute_metrics(df):
    time_saved = (df["time_without_ai"] - df["time_with_ai"]).sum()

    error_reduction = (
                              (df["errors_without_ai"].sum() - df["errors_with_ai"].sum())
                              / df["errors_without_ai"].sum()
                      ) * 100

    productivity_score = min(100, int((time_saved * 2) + (error_reduction)))

    ai_usage_map = {"Low": 1, "Medium": 2, "High": 3}
    df["ai_usage_num"] = df["ai_usage"].map(ai_usage_map)

    ai_usage_rate = (df["ai_usage_num"].mean() / 3) * 100

    return {
        "time_saved": time_saved,
        "error_reduction": error_reduction,
        "tasks_completed": len(df),
        "productivity_score": productivity_score,
        "ai_usage_rate": ai_usage_rate
    }