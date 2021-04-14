"""Calculates basics statistics for each attribute, chart and datapoint in
the 'live' task across both study conditions.

Saves attribute table, chart table, and datapoint table to CSV per participant.
"""
import os
import json
import ast

import pandas as pd
import numpy as np

from constants import ATTRIBUTES, IDS

#
# ---------------------------- INTERACTION TYPES -----------------------------
# SUBMIT BUTTONS
#   CLICK_SUBMIT_BUTTON_INITIAL = "click_submit_button_initial",
#   CLICK_SUBMIT_BUTTON_REVISE = "click_submit_button_revise",
#   CLICK_SUBMIT_BUTTON_FINAL = "click_submit_button_final",
# CLICKING ON THE TAGS IN THE DISTRIBUTION PANEL (RT/RTSUM ONLY)
#   CHANGE_ATTRIBUTE_DISTRIBUTION_RESULTS = "change_attribute_distribution_results",
#   CHANGE_ATTRIBUTE_DISTRIBUTION = "change_attribute_distribution",
# ENCODE/FILTER
#   CHANGE_FILTER = "filter_changed",
#   CHANGE_AXIS_ATTRIBUTE = "axes_attribute_changed",
# SELECTION INTERACTIONS
#   ADD_TO_LIST_VIA_SCATTERPLOT_CLICK = "add_to_list_via_scatterplot_click",
#   ADD_TO_LIST_VIA_CARD_CLICK = "add_to_list_via_card_click",
#   REMOVE_FROM_LIST_VIA_LIST_ITEM_CLICK = "remove_from_list_via_list_item_click",
#   REMOVE_FROM_LIST_VIA_CARD_CLICK = "remove_from_list_via_card_click",
# HOVER INTERACTIONS
#   MOUSEOUT_FROM_LIST = "mouseout_from_list",
#   MOUSEOVER_FROM_LIST = "mouseover_from_list",
#   MOUSEOVER_ON_SCATTERPLOT_POINT = "mouseover",
#   MOUSEOUT_FROM_SCATTERPLOT_POINT = "mouseout",
#


def get_dict(x):
    try:
        return ast.literal_eval(str(x))
    except Exception as e:
        return np.NaN


def get_list(x):
    try:
        return ast.literal_eval(str(x))
    except Exception as e:
        return []


def get_attr_stats(df, df_ts, task, pid):
    """(12) Attributes / Encodings Panel Measures:
    - (2) Count attribute encoded/filtered
    - (2) Total, average duration attribute encoded
    - (8) Avg/Final metric values
    """
    # Get task starting and ending timestamps
    task_start_ts = df_ts.set_index("activities").at[f"task-{task}", "epoch_timestamp"]
    task_end_ts = df_ts.set_index("activities").at[f"live-{task}", "epoch_timestamp"]

    # Create attribute zeros dataframe for concating with results
    attr_zeros = pd.DataFrame(
        {
            "attribute": ATTRIBUTES[task]["all"],
            "count_encode_changed": [0 for _ in range(len(ATTRIBUTES[task]["all"]))],
            "total_attr_encode_ms": [0 for _ in range(len(ATTRIBUTES[task]["all"]))],
            "avg_attr_encode_ms": [0 for _ in range(len(ATTRIBUTES[task]["all"]))],
            "count_filter_changed": [0 for _ in range(len(ATTRIBUTES[task]["all"]))],
            "count_dist_card_click": [0 for _ in range(len(ATTRIBUTES[task]["all"]))],
            "ac_metric_avg": [0 for _ in range(len(ATTRIBUTES[task]["all"]))],
            "ac_metric_final": [0 for _ in range(len(ATTRIBUTES[task]["all"]))],
            "ad_metric_avg": [0 for _ in range(len(ATTRIBUTES[task]["all"]))],
            "ad_metric_final": [0 for _ in range(len(ATTRIBUTES[task]["all"]))],
            "dpc_metric_avg": [0 for _ in range(len(ATTRIBUTES[task]["all"]))],
            "dpc_metric_final": [0 for _ in range(len(ATTRIBUTES[task]["all"]))],
            "dpd_metric_avg": [0 for _ in range(len(ATTRIBUTES[task]["all"]))],
            "dpd_metric_final": [0 for _ in range(len(ATTRIBUTES[task]["all"]))],
        }
    )

    # task drop cols
    drop_cols = {"politics": ["id", "first_name", "last_name"], "movies": ["id", "Title"]}

    # ======================================================================= #

    # Get all encoding set interactions
    mask = df["interactionType"] == "axes_attribute_changed"
    attr_changed = df[mask]
    if len(attr_changed.index) > 0:
        attr_changed = attr_changed[["interactionAt", "interactionType", "x", "y"]]
        x_changed = pd.concat(
            [
                attr_changed[["interactionAt", "interactionType", "x"]],
                attr_changed["x"].ne(attr_changed["x"].shift()).astype(int).rename("changed"),
            ],
            axis=1,
        )
        x_changed = (
            x_changed[x_changed["changed"] != 0]
            .drop(columns=["changed"])
            .assign(measurement=lambda x: "x_axis_set")
            .rename(columns={"x": "attribute"})
        )
        x_changed_dup = pd.DataFrame(np.repeat(x_changed.values, 2, axis=0))
        x_changed_dup.columns = x_changed.columns
        df_x_changed = pd.concat(
            [
                x_changed_dup[["attribute", "measurement"]],
                x_changed_dup["interactionAt"].shift(-1).fillna(task_end_ts),
            ],
            axis=1,
        ).dropna(subset=["attribute"])
        df_x_changed["value"] = df_x_changed.index % 2 == 0
        y_changed = pd.concat(
            [
                attr_changed[["interactionAt", "interactionType", "y"]],
                attr_changed["y"].ne(attr_changed["y"].shift()).astype(int).rename("changed"),
            ],
            axis=1,
        )
        y_changed = (
            y_changed[y_changed["changed"] != 0]
            .drop(columns=["changed"])
            .assign(measurement=lambda x: "y_axis_set")
            .rename(columns={"y": "attribute"})
        )
        y_changed_dup = pd.DataFrame(np.repeat(y_changed.values, 2, axis=0))
        y_changed_dup.columns = y_changed.columns
        df_y_changed = pd.concat(
            [
                y_changed_dup[["attribute", "measurement"]],
                y_changed_dup["interactionAt"].shift(-1).fillna(task_end_ts),
            ],
            axis=1,
        ).dropna(subset=["attribute"])
        df_y_changed["value"] = df_y_changed.index % 2 == 0
        axis_set = (
            pd.concat([df_x_changed, df_y_changed])
            .sort_values(by=["attribute", "measurement", "interactionAt"])
            .reset_index(drop=True)
        )
    else:
        axis_set = pd.DataFrame(None, columns=["attribute", "measurement", "interactionAt", "value"])

    if len(axis_set.index) > 0:
        # Get encoding set counts
        encode_count = (
            axis_set[axis_set["value"]]
            .groupby(["attribute"])
            .size()
            .reset_index()
            .rename(columns={0: "count_encode_changed"})
        )
        # concat counted attributes with all attributes and drop duplicates from zeros dataframe
        df_encode_count = (
            pd.concat(
                [
                    encode_count,
                    attr_zeros[["attribute", "count_encode_changed"]],
                ]
            )
            .drop_duplicates("attribute", keep="first")
            .reset_index(drop=True)
        )

        # Get avg/total time attributes were encoded
        attr_encode_time_rows = []
        for key, grp in axis_set.groupby(["attribute"]):
            attr_encode_ms = []  # keep list of encoding set times in ms
            grp_pivot = grp.pivot(index="interactionAt", columns="measurement", values="value")
            if "x_axis_set" in grp_pivot.columns:
                grp_x_axis_set = grp_pivot["x_axis_set"].dropna()  # only keep non-nan values
                for index, value in grp_x_axis_set.items():
                    if value:
                        start = index  # value == True => encoding added
                    else:
                        stop = index  # value == False => encoding removed
                        elapsed = stop - start
                        attr_encode_ms.append(elapsed)
                        if elapsed < 0:
                            print(f"[WARN] {pid} had negative encode time elapsed.")
            if "y_axis_set" in grp_pivot.columns:
                grp_y_axis_set = grp_pivot["y_axis_set"].dropna()  # only keep non-nan values
                for index, value in grp_y_axis_set.items():
                    if value:
                        start = index  # value == True => encoding added
                    else:
                        stop = index  # value == False => encoding removed
                        elapsed = stop - start
                        attr_encode_ms.append(elapsed)
                        if elapsed < 0:
                            print(f"[WARN] {pid} had negative attr encode time elapsed.")
            sum_encode_ms = np.sum(attr_encode_ms)
            avg_encode_ms = np.average(attr_encode_ms)
            if sum_encode_ms > 3600000:
                print(f"[WARN] {pid} had attr encode time over 1 hour.")
            attr_encode_time_rows.append([key, sum_encode_ms, avg_encode_ms])
        attr_encode_time = pd.DataFrame(
            attr_encode_time_rows, columns=["attribute", "total_attr_encode_ms", "avg_attr_encode_ms"]
        )
        # concat avg/total time encode set per attribute with all attributes and drop duplicates from zeros dataframe
        df_attr_encode_time = (
            pd.concat(
                [
                    attr_encode_time,
                    attr_zeros[["attribute", "total_attr_encode_ms", "avg_attr_encode_ms"]],
                ]
            )
            .drop_duplicates("attribute", keep="first")
            .reset_index(drop=True)
        )
    else:
        # no interactions like this => use zeros dataframe
        df_encode_count = attr_zeros[["attribute", "count_encode_changed"]]
        df_attr_encode_time = attr_zeros[["attribute", "total_attr_encode_ms", "avg_attr_encode_ms"]]

    # ======================================================================= #

    # Get filter attribute changed count
    mask = df["interactionType"] == "filter_changed"
    filter_changed = df[mask]
    if len(filter_changed.index) > 0:
        # group by attribute and count interactions
        attr_filter_changed_count = (
            filter_changed.groupby(["attribute"]).size().reset_index().rename(columns={0: "count_filter_changed"})
        )
        # concat counted attributes with all attributes and drop duplicates from zeros dataframe
        df_filter_changed_count = (
            pd.concat([attr_filter_changed_count, attr_zeros[["attribute", "count_filter_changed"]]])
            .drop_duplicates("attribute", keep="first")
            .reset_index(drop=True)
        )
    else:
        # no interactions like this => use zeros dataframe
        df_filter_changed_count = attr_zeros[["attribute", "count_filter_changed"]]

    # ======================================================================= #

    # Get distribution panel card click counts
    mask = df["interactionType"] == "change_attribute_distribution"
    dist_card_click = df[mask]
    if len(dist_card_click.index) > 0:
        # group by attribute and count interactions
        attr_dist_card_click_count = (
            dist_card_click.groupby(["attribute"]).size().reset_index().rename(columns={0: "count_dist_card_click"})
        )
        # concat counted attributes with all attributes and drop duplicates from zeros dataframe
        df_dist_card_click_count = (
            pd.concat([attr_dist_card_click_count, attr_zeros[["attribute", "count_dist_card_click"]]])
            .drop_duplicates("attribute", keep="first")
            .reset_index(drop=True)
        )
    else:
        # no interactions like this => use zeros dataframe
        df_dist_card_click_count = attr_zeros[["attribute", "count_dist_card_click"]]

    # ======================================================================= #

    # get average/final focus metrics for each attribute
    focus_metrics = df[["ac_metric", "ad_metric", "dpc_metric", "dpd_metric"]].dropna()
    if len(focus_metrics.index) > 0:
        # AC METRIC AVG/FINAL
        ac_metric = focus_metrics["ac_metric"].map(lambda x: get_dict(x)).apply(pd.Series).drop(columns=drop_cols[task])
        df_ac_metric_avg = (
            pd.concat(
                [
                    ac_metric.mean(axis=0).reset_index().rename(columns={"index": "attribute", 0: "ac_metric_avg"}),
                    attr_zeros[["attribute", "ac_metric_avg"]],
                ]
            )
            .drop_duplicates("attribute", keep="first")
            .reset_index(drop=True)
        )
        df_ac_metric_final = (
            pd.concat(
                [
                    ac_metric.iloc[-1]
                    .rename(0)
                    .T.reset_index()
                    .rename(columns={"index": "attribute", 0: "ac_metric_final"}),
                    attr_zeros[["attribute", "ac_metric_final"]],
                ]
            )
            .drop_duplicates("attribute", keep="first")
            .reset_index(drop=True)
        )
        # AD METRIC AVG/FINAL
        ad_metric = focus_metrics["ad_metric"].map(lambda x: get_dict(x)).apply(pd.Series).drop(columns=drop_cols[task])
        df_ad_metric_avg = (
            pd.concat(
                [
                    ad_metric.mean(axis=0).reset_index().rename(columns={"index": "attribute", 0: "ad_metric_avg"}),
                    attr_zeros[["attribute", "ad_metric_avg"]],
                ]
            )
            .drop_duplicates("attribute", keep="first")
            .reset_index(drop=True)
        )
        df_ad_metric_final = (
            pd.concat(
                [
                    ad_metric.iloc[-1]
                    .rename(0)
                    .T.reset_index()
                    .rename(columns={"index": "attribute", 0: "ad_metric_final"}),
                    attr_zeros[["attribute", "ad_metric_final"]],
                ]
            )
            .drop_duplicates("attribute", keep="first")
            .reset_index(drop=True)
        )
        # DPC METRIC AVG/FINAL
        dpd_metric = focus_metrics["dpd_metric"]
        df_dpd_metric_avg = pd.DataFrame(
            {
                "attribute": ATTRIBUTES[task]["all"],
                "dpd_metric_avg": [dpd_metric.mean(axis=0) for _ in range(len(ATTRIBUTES[task]["all"]))],
            }
        )
        df_dpd_metric_final = pd.DataFrame(
            {
                "attribute": ATTRIBUTES[task]["all"],
                "dpd_metric_final": [dpd_metric.iloc[-1] for _ in range(len(ATTRIBUTES[task]["all"]))],
            }
        )
        # DPC METRIC AVG/FINAL
        dpc_metric = focus_metrics["dpc_metric"]
        df_dpc_metric_avg = pd.DataFrame(
            {
                "attribute": ATTRIBUTES[task]["all"],
                "dpc_metric_avg": [dpc_metric.mean(axis=0) for _ in range(len(ATTRIBUTES[task]["all"]))],
            }
        )
        df_dpc_metric_final = pd.DataFrame(
            {
                "attribute": ATTRIBUTES[task]["all"],
                "dpc_metric_final": [dpc_metric.iloc[-1] for _ in range(len(ATTRIBUTES[task]["all"]))],
            }
        )
    else:
        # missing focus metrics => use zeros dataframe
        df_ac_metric_avg = attr_zeros[["attribute", "ac_metric_avg"]]
        df_ac_metric_final = attr_zeros[["attribute", "ac_metric_final"]]
        df_ad_metric_avg = attr_zeros[["attribute", "ad_metric_avg"]]
        df_ad_metric_final = attr_zeros[["attribute", "ad_metric_final"]]
        df_dpd_metric_avg = attr_zeros[["attribute", "dpd_metric_avg"]]
        df_dpd_metric_final = attr_zeros[["attribute", "dpd_metric_final"]]
        df_dpc_metric_avg = attr_zeros[["attribute", "dpc_metric_avg"]]
        df_dpc_metric_final = attr_zeros[["attribute", "dpc_metric_final"]]

    # ======================================================================= #

    # Combine attribute encode, filter, card toggle and pin dataframes
    dfs = [
        df_encode_count,
        df_attr_encode_time,
        df_filter_changed_count,
        df_dist_card_click_count,
        df_ac_metric_avg,
        df_ac_metric_final,
        df_ad_metric_avg,
        df_ad_metric_final,
        df_dpd_metric_avg,
        df_dpd_metric_final,
        df_dpc_metric_avg,
        df_dpc_metric_final,
    ]
    dfs = [df.set_index("attribute", drop=True).sort_index() for df in dfs]
    df_attr = pd.concat(dfs, axis=1, join="outer", copy=False).reset_index(drop=False)

    return df_attr


def get_datapoint_stats(df, df_ts, task):
    """(6) Data Point (VIS Panel + Details Table) Statistics:
    - (2) Count of datapoint hovers -- group by vis/list
    - (4) Count of datapoint clicks -- group by add/remove => vis/list
    """
    # Get task starting and ending timestamps
    task_start_ts = df_ts.set_index("activities").at[f"task-{task}", "epoch_timestamp"]
    task_end_ts = df_ts.set_index("activities").at[f"live-{task}", "epoch_timestamp"]

    # Create hover zeros dataframe for concating with results
    hover_zeros = pd.DataFrame(
        {
            "id": IDS[task],
            "count_vis_hovers": [0 for _ in range(len(IDS[task]))],
            "count_vis_click_add": [0 for _ in range(len(IDS[task]))],
            "count_list_hovers": [0 for _ in range(len(IDS[task]))],
            "count_list_click_remove": [0 for _ in range(len(IDS[task]))],
            "count_card_click_add": [0 for _ in range(len(IDS[task]))],
            "count_card_click_remove": [0 for _ in range(len(IDS[task]))],
        }
    )

    # ======================================================================= #

    # get vis hovers count
    mask = df["interactionType"] == "mouseout"
    vis_hovers = df[mask]
    if len(vis_hovers.index) > 0:
        # unpack the x and y columns
        dfx = (
            vis_hovers["x"]
            .map(lambda x: get_dict(x))
            .apply(pd.Series)
            .rename(columns={"name": "x_name", "value": "x_value"})
        )
        dfy = (
            vis_hovers["y"]
            .map(lambda x: get_dict(x))
            .apply(pd.Series)
            .rename(columns={"name": "y_name", "value": "y_value"})
        )
        vis_hovers_xy = pd.concat([vis_hovers.drop(columns=["x", "y"]), dfx, dfy], axis=1)
        if len(vis_hovers_xy.index) > 0:
            # group by id to get the counts
            vis_hover_count = vis_hovers_xy.groupby(["id"]).size().reset_index().rename(columns={0: "count_vis_hovers"})
            # concat ids with vis hovers with all ids and drop duplicates from zeros dataframe
            df_vis_hovers_count = (
                pd.concat([vis_hover_count, hover_zeros[["id", "count_vis_hovers"]]])
                .drop_duplicates("id", keep="first")
                .reset_index(drop=True)
            )
        else:
            # no interactions like this => use zeros dataframe
            df_vis_hovers_count = hover_zeros[["id", "count_vis_hovers"]]
    else:
        # no interactions like this => use zeros dataframe
        df_vis_hovers_count = hover_zeros[["id", "count_vis_hovers"]]

    # get vis click add count
    mask = df["interactionType"] == "add_to_list_via_scatterplot_click"
    vis_click_add = df[mask]
    if len(vis_click_add.index) > 0:
        # unpack the x and y columns
        dfx = (
            vis_click_add["x"]
            .map(lambda x: get_dict(x))
            .apply(pd.Series)
            .rename(columns={"name": "x_name", "value": "x_value"})
        )
        dfy = (
            vis_click_add["y"]
            .map(lambda x: get_dict(x))
            .apply(pd.Series)
            .rename(columns={"name": "y_name", "value": "y_value"})
        )
        vis_click_add_xy = pd.concat([vis_click_add.drop(columns=["x", "y"]), dfx, dfy], axis=1)
        if len(vis_click_add_xy.index) > 0:
            # group by id to get the counts
            vis_click_add_count = (
                vis_click_add_xy.groupby(["id"]).size().reset_index().rename(columns={0: "count_vis_click_add"})
            )
            # concat ids with list hovers with all ids and drop duplicates from zeros dataframe
            df_vis_click_add_count = (
                pd.concat([vis_click_add_count, hover_zeros[["id", "count_vis_click_add"]]])
                .drop_duplicates("id", keep="first")
                .reset_index(drop=True)
            )
        else:
            # no interactions like this => use zeros dataframe
            df_vis_click_add_count = hover_zeros[["id", "count_vis_click_add"]]
    else:
        # no interactions like this => use zeros dataframe
        df_vis_click_add_count = hover_zeros[["id", "count_vis_click_add"]]

    # ======================================================================= #

    # get list hovers count
    mask = df["interactionType"] == "mouseout_from_list"
    list_hovers = df[mask]
    if len(list_hovers.index) > 0:
        # unpack the x and y columns
        dfx = (
            list_hovers["x"]
            .map(lambda x: get_dict(x))
            .apply(pd.Series)
            .rename(columns={"name": "x_name", "value": "x_value"})
        )
        dfy = (
            list_hovers["y"]
            .map(lambda x: get_dict(x))
            .apply(pd.Series)
            .rename(columns={"name": "y_name", "value": "y_value"})
        )
        list_hovers_xy = pd.concat([list_hovers.drop(columns=["x", "y"]), dfx, dfy], axis=1)
        if len(list_hovers_xy.index) > 0:
            # group by id to get the counts
            list_hover_count = (
                list_hovers_xy.groupby(["id"]).size().reset_index().rename(columns={0: "count_list_hovers"})
            )
            # concat ids with list hovers with all ids and drop duplicates from zeros dataframe
            df_list_hovers_count = (
                pd.concat([list_hover_count, hover_zeros[["id", "count_list_hovers"]]])
                .drop_duplicates("id", keep="first")
                .reset_index(drop=True)
            )
        else:
            # no interactions like this => use zeros dataframe
            df_list_hovers_count = hover_zeros[["id", "count_list_hovers"]]
    else:
        # no interactions like this => use zeros dataframe
        df_list_hovers_count = hover_zeros[["id", "count_list_hovers"]]

    # get list click remove count
    mask = df["interactionType"] == "remove_from_list_via_list_item_click"
    list_click_remove = df[mask]
    if len(list_click_remove.index) > 0:
        # unpack the x and y columns
        dfx = (
            list_click_remove["x"]
            .map(lambda x: get_dict(x))
            .apply(pd.Series)
            .rename(columns={"name": "x_name", "value": "x_value"})
        )
        dfy = (
            list_click_remove["y"]
            .map(lambda x: get_dict(x))
            .apply(pd.Series)
            .rename(columns={"name": "y_name", "value": "y_value"})
        )
        list_click_remove_xy = pd.concat([list_click_remove.drop(columns=["x", "y"]), dfx, dfy], axis=1)
        if len(list_click_remove_xy.index) > 0:
            # group by id to get the counts
            list_click_remove_count = (
                list_click_remove_xy.groupby(["id"]).size().reset_index().rename(columns={0: "count_list_click_remove"})
            )
            # concat ids with list click_remove with all ids and drop duplicates from zeros dataframe
            df_list_click_remove_count = (
                pd.concat([list_click_remove_count, hover_zeros[["id", "count_list_click_remove"]]])
                .drop_duplicates("id", keep="first")
                .reset_index(drop=True)
            )
        else:
            # no interactions like this => use zeros dataframe
            df_list_click_remove_count = hover_zeros[["id", "count_list_click_remove"]]
    else:
        # no interactions like this => use zeros dataframe
        df_list_click_remove_count = hover_zeros[["id", "count_list_click_remove"]]

    # ======================================================================= #

    # get card click add count
    mask = df["interactionType"] == "add_to_list_via_card_click"
    card_click_add = df[mask]
    if len(card_click_add.index) > 0:
        # unpack the x and y columns
        dfx = (
            card_click_add["x"]
            .map(lambda x: get_dict(x))
            .apply(pd.Series)
            .rename(columns={"name": "x_name", "value": "x_value"})
        )
        dfy = (
            card_click_add["y"]
            .map(lambda x: get_dict(x))
            .apply(pd.Series)
            .rename(columns={"name": "y_name", "value": "y_value"})
        )
        card_click_add_xy = pd.concat([card_click_add.drop(columns=["x", "y"]), dfx, dfy], axis=1)
        if len(card_click_add_xy.index) > 0:
            # group by id to get the counts
            card_click_add_count = (
                card_click_add_xy.groupby(["id"]).size().reset_index().rename(columns={0: "count_card_click_add"})
            )
            # concat ids with card click_add with all ids and drop duplicates from zeros dataframe
            df_card_click_add_count = (
                pd.concat([card_click_add_count, hover_zeros[["id", "count_card_click_add"]]])
                .drop_duplicates("id", keep="first")
                .reset_index(drop=True)
            )
        else:
            # no interactions like this => use zeros dataframe
            df_card_click_add_count = hover_zeros[["id", "count_card_click_add"]]
    else:
        # no interactions like this => use zeros dataframe
        df_card_click_add_count = hover_zeros[["id", "count_card_click_add"]]

    # get card click remove count
    mask = df["interactionType"] == "remove_from_list_via_card_click"
    card_click_remove = df[mask]
    if len(card_click_remove.index) > 0:
        # unpack the x and y columns
        dfx = (
            card_click_remove["x"]
            .map(lambda x: get_dict(x))
            .apply(pd.Series)
            .rename(columns={"name": "x_name", "value": "x_value"})
        )
        dfy = (
            card_click_remove["y"]
            .map(lambda x: get_dict(x))
            .apply(pd.Series)
            .rename(columns={"name": "y_name", "value": "y_value"})
        )
        card_click_remove_xy = pd.concat([card_click_remove.drop(columns=["x", "y"]), dfx, dfy], axis=1)
        if len(card_click_remove_xy.index) > 0:
            # group by id to get the counts
            card_click_remove_count = (
                card_click_remove_xy.groupby(["id"]).size().reset_index().rename(columns={0: "count_card_click_remove"})
            )
            # concat ids with card click_remove with all ids and drop duplicates from zeros dataframe
            df_card_click_remove_count = (
                pd.concat([card_click_remove_count, hover_zeros[["id", "count_card_click_remove"]]])
                .drop_duplicates("id", keep="first")
                .reset_index(drop=True)
            )
        else:
            # no interactions like this => use zeros dataframe
            df_card_click_remove_count = hover_zeros[["id", "count_card_click_remove"]]
    else:
        # no interactions like this => use zeros dataframe
        df_card_click_remove_count = hover_zeros[["id", "count_card_click_remove"]]

    # ======================================================================= #

    # Combine unit, row, and agg hover counts dataframes
    dfs = [
        df_vis_hovers_count,
        df_vis_click_add_count,
        df_list_hovers_count,
        df_list_click_remove_count,
        df_card_click_add_count,
        df_card_click_remove_count,
    ]
    dfs = [df.set_index("id", drop=True).sort_index() for df in dfs]
    df_datapoint = pd.concat(dfs, axis=1, join="outer", copy=False).reset_index(drop=False)

    return df_datapoint


# get files object
with open("output_file_locations.json", "r") as f:
    files = json.load(f)

AYS_PIDS = files["AYS"]["participants"]
SUM_PIDS = files["SUM"]["participants"]
RT_PIDS = files["RT"]["participants"]
RTSUM_PIDS = files["RTSUM"]["participants"]

TASKS = ["politics", "movies"]

DATA_META_COLS = [
    "ac_details",
    "ad_details",
    "dpd_details",
    "dpc_details",
]


# ================================= AYS ================================= #

print("AYS")
for task in TASKS:
    # lists of dataframes to combine into master file at the end per task
    ays_attr_dfs = []
    ays_datapoint_dfs = []

    # Loop through particpants
    for pid in AYS_PIDS:
        basepath = os.path.join("CTRL", pid)  # basepath for PID
        print(f"  calculating {task} stats for AYS PID {pid} ...")
        df = pd.read_csv(os.path.join(basepath, f"interaction.csv")).drop(columns=DATA_META_COLS)
        df_task = df[df["appMode"] == task].reset_index(drop=True).drop(columns=["appMode"])
        if pid == "EPcW0vyMy901":
            df_task["interactionAt"] -= 7 * 3600000  # summary.json is GMT-07:00 for some reason
        else:
            df_task["interactionAt"] -= 4 * 3600000  # convert EPOCH timestamp from GMT to EDT (GMT-04:00)
        df_ts = pd.read_csv(os.path.join(basepath, "timestamps.csv"))
        # get ATTRIBUTE-level statistics
        df_attr = get_attr_stats(df_task, df_ts, task, pid)
        df_attr.to_csv(os.path.join(basepath, f"attr_stats_{task}.csv"), index=False)
        df_attr.insert(0, "pid", pd.Series([pid for _ in range(len(ATTRIBUTES[task]["all"]))]))
        ays_attr_dfs.append(df_attr)
        # get DATAPOINT-level statistics
        df_datapoint = get_datapoint_stats(df_task, df_ts, task)
        df_datapoint.to_csv(os.path.join(basepath, f"datapoint_stats_{task}.csv"), index=False)
        df_datapoint.insert(0, "pid", pd.Series([pid for _ in range(len(IDS[task]))]))
        ays_datapoint_dfs.append(df_datapoint)

    # combine collected dataframes into master file at the end
    df_ays_attr = pd.concat(ays_attr_dfs)
    df_ays_attr.to_csv(os.path.join("CTRL", f"all_CTRL_{task}_attr_stats.csv"), index=False)
    df_ays_datapoint = pd.concat(ays_datapoint_dfs)
    df_ays_datapoint.to_csv(os.path.join("CTRL", f"all_CTRL_{task}_datapoint_stats.csv"), index=False)

# ================================= SUM ================================= #

print("SUM")
for task in TASKS:
    # lists of dataframes to combine into master file at the end per task
    sum_attr_dfs = []
    sum_datapoint_dfs = []

    # Loop through particpants
    for pid in SUM_PIDS:
        basepath = os.path.join("SUM", pid)  # basepath for PID
        print(f"  calculating {task} stats for SUM PID {pid} ...")
        df = pd.read_csv(os.path.join(basepath, f"interaction.csv")).drop(columns=DATA_META_COLS)
        df_task = df[df["appMode"] == task].reset_index(drop=True).drop(columns=["appMode"])
        df_task["interactionAt"] -= 4 * 3600000  # convert EPOCH timestamp from GMT to EDT (GMT-04:00)
        df_ts = pd.read_csv(os.path.join(basepath, "timestamps.csv"))
        # get ATTRIBUTE-level statistics
        df_attr = get_attr_stats(df_task, df_ts, task, pid)
        df_attr.to_csv(os.path.join(basepath, f"attr_stats_{task}.csv"), index=False)
        df_attr.insert(0, "pid", pd.Series([pid for _ in range(len(ATTRIBUTES[task]["all"]))]))
        sum_attr_dfs.append(df_attr)
        # get DATAPOINT-level statistics
        df_datapoint = get_datapoint_stats(df_task, df_ts, task)
        df_datapoint.to_csv(os.path.join(basepath, f"datapoint_stats_{task}.csv"), index=False)
        df_datapoint.insert(0, "pid", pd.Series([pid for _ in range(len(IDS[task]))]))
        sum_datapoint_dfs.append(df_datapoint)

    # combine collected dataframes into master file at the end
    df_sum_attr = pd.concat(sum_attr_dfs)
    df_sum_attr.to_csv(os.path.join("SUM", f"all_SUM_{task}_attr_stats.csv"), index=False)
    df_sum_datapoint = pd.concat(sum_datapoint_dfs)
    df_sum_datapoint.to_csv(os.path.join("SUM", f"all_SUM_{task}_datapoint_stats.csv"), index=False)

# ================================= RT ================================= #

print("RT")
for task in TASKS:
    # lists of dataframes to combine into master file at the end per task
    rt_attr_dfs = []
    rt_datapoint_dfs = []

    # Loop through particpants
    for pid in RT_PIDS:
        basepath = os.path.join("RT", pid)  # basepath for PID
        print(f"  calculating {task} stats for RT PID {pid} ...")
        df = pd.read_csv(os.path.join(basepath, f"interaction.csv")).drop(columns=DATA_META_COLS)
        df_task = df[df["appMode"] == task].reset_index(drop=True).drop(columns=["appMode"])
        df_task["interactionAt"] -= 4 * 3600000  # convert EPOCH timestamp from GMT to EDT (GMT-04:00)
        df_ts = pd.read_csv(os.path.join(basepath, "timestamps.csv"))
        # get ATTRIBUTE-level statistics
        df_attr = get_attr_stats(df_task, df_ts, task, pid)
        df_attr.to_csv(os.path.join(basepath, f"attr_stats_{task}.csv"), index=False)
        df_attr.insert(0, "pid", pd.Series([pid for _ in range(len(ATTRIBUTES[task]["all"]))]))
        rt_attr_dfs.append(df_attr)
        # get DATAPOINT-level statistics
        df_datapoint = get_datapoint_stats(df_task, df_ts, task)
        df_datapoint.to_csv(os.path.join(basepath, f"datapoint_stats_{task}.csv"), index=False)
        df_datapoint.insert(0, "pid", pd.Series([pid for _ in range(len(IDS[task]))]))
        rt_datapoint_dfs.append(df_datapoint)

    # combine collected dataframes into master file at the end
    df_rt_attr = pd.concat(rt_attr_dfs)
    df_rt_attr.to_csv(os.path.join("RT", f"all_RT_{task}_attr_stats.csv"), index=False)
    df_rt_datapoint = pd.concat(rt_datapoint_dfs)
    df_rt_datapoint.to_csv(os.path.join("RT", f"all_RT_{task}_datapoint_stats.csv"), index=False)

# ================================= RTSUM ================================= #

print("RTSUM")
for task in TASKS:
    # lists of dataframes to combine into master file at the end per task
    rtsum_attr_dfs = []
    rtsum_datapoint_dfs = []

    # Loop through particpants
    for pid in RTSUM_PIDS:
        basepath = os.path.join("RTSUM", pid)  # basepath for PID
        print(f"  calculating {task} stats for RTSUM PID {pid} ...")
        df = pd.read_csv(os.path.join(basepath, f"interaction.csv")).drop(columns=DATA_META_COLS)
        df_task = df[df["appMode"] == task].reset_index(drop=True).drop(columns=["appMode"])
        df_task["interactionAt"] -= 4 * 3600000  # convert EPOCH timestamp from GMT to EDT (GMT-04:00)
        df_ts = pd.read_csv(os.path.join(basepath, "timestamps.csv"))
        # get ATTRIBUTE-level statistics
        df_attr = get_attr_stats(df_task, df_ts, task, pid)
        df_attr.to_csv(os.path.join(basepath, f"attr_stats_{task}.csv"), index=False)
        df_attr.insert(0, "pid", pd.Series([pid for _ in range(len(ATTRIBUTES[task]["all"]))]))
        rtsum_attr_dfs.append(df_attr)
        # get DATAPOINT-level statistics
        df_datapoint = get_datapoint_stats(df_task, df_ts, task)
        df_datapoint.to_csv(os.path.join(basepath, f"datapoint_stats_{task}.csv"), index=False)
        df_datapoint.insert(0, "pid", pd.Series([pid for _ in range(len(IDS[task]))]))
        rtsum_datapoint_dfs.append(df_datapoint)

    # combine collected dataframes into master file at the end
    df_rtsum_attr = pd.concat(rtsum_attr_dfs)
    df_rtsum_attr.to_csv(os.path.join("RTSUM", f"all_RTSUM_{task}_attr_stats.csv"), index=False)
    df_rtsum_datapoint = pd.concat(rtsum_datapoint_dfs)
    df_rtsum_datapoint.to_csv(os.path.join("RTSUM", f"all_RTSUM_{task}_datapoint_stats.csv"), index=False)
