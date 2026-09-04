import pandas as pd


class MaintenanceAnalytics:

    def get_summary(self, df):

        summary = {
            "total_records": len(df),
            "total_failures": int(
                df["Machine failure"].sum()
            ),
            "failure_rate": round(
                df["Machine failure"].mean() * 100,
                2
            ),
            "average_air_temperature": round(
                df["Air temperature [K]"].mean(),
                2
            ),
            "average_process_temperature": round(
                df["Process temperature [K]"].mean(),
                2
            ),
            "average_rotational_speed": round(
                df["Rotational speed [rpm]"].mean(),
                2
            ),
            "average_torque": round(
                df["Torque [Nm]"].mean(),
                2
            ),
            "average_tool_wear": round(
                df["Tool wear [min]"].mean(),
                2
            )
        }

        return summary


    def get_machine_type_analysis(self, df):

        type_analysis = (
            df.groupby("Type")
            .agg(
                total_machines=(
                    "Machine failure",
                    "count"
                ),
                failures=(
                    "Machine failure",
                    "sum"
                ),
                failure_rate=(
                    "Machine failure",
                    "mean"
                )
            )
            .reset_index()
        )

        type_analysis[
            "failure_rate"
        ] = (
            type_analysis[
                "failure_rate"
            ] * 100
        ).round(2)

        return type_analysis


    def get_failure_type_analysis(self, df):

        failure_columns = [
            "TWF",
            "HDF",
            "PWF",
            "OSF",
            "RNF"
        ]

        failure_counts = {}

        for column in failure_columns:

            failure_counts[column] = int(
                df[column].sum()
            )

        failure_df = pd.DataFrame(
            list(failure_counts.items()),
            columns=[
                "failure_type",
                "count"
            ]
        )

        return failure_df.sort_values(
            by="count",
            ascending=False
        )