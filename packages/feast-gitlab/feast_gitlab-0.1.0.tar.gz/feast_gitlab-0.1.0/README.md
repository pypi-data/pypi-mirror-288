This is a fork of the Feast project. Specifically of version 0.40. You can see the Readme for that version [here](https://github.com/feast-dev/feast/tree/v0.40-branch).

This fork introduces a functionality that is useful for the Data Science team at Gitlab.

This functionality is jinja templating for the SQL queries defined in the data sources.

# Motivation

Because Feast as of this moment does not support batch transformations we have been using the data sources SQL query definitions as a place to perform some aggregations and sliding windows transformations. The problem is that said transformations became not performant when we had high granularity data, as we need to create a table that contains all of the entities for all period of times.

This is very compute heavy since we are creating records that will not be used.

# Solution

Add jinja templating to data source queries. This would let us access the `entity_dataframe` and go from queries like this:

```sql
WITH base AS (

    SELECT *
    FROM  prod.workspace_data_science.monthly_stage_usage_by_account

), dim_date AS (

    SELECT first_day_of_month AS snapshot_month
    FROM prod.common.dim_date
    WHERE date_actual <= CURRENT_DATE
        AND date_actual >= '2021-02-01'::DATE

), scaffold AS (

    SELECT DISTINCT
        base.dim_crm_account_id,
        dim_date.snapshot_month 
    FROM base 
    CROSS JOIN dim_date
)

SELECT
    a.dim_crm_account_id,
    a.snapshot_month AS product_usage_date,
    --number of all time features used
    SUM(b.stage_create_alltime_features) AS stage_create_alltime_features_cnt,

FROM scaffold a
LEFT JOIN base b
      ON a.dim_crm_account_id = b.dim_crm_account_id 
      AND b.snapshot_month BETWEEN ADD_MONTHS(a.snapshot_month, -{period_unit}) AND a.snapshot_month
GROUP BY 1, 2, 3
```

To queries like this:

```sql
-- USE_TEMPLATE_WORKFLOW
WITH base AS (
    SELECT *
    FROM  prod.workspace_data_science.monthly_stage_usage_by_account
    {% if validation %}
    LIMIT 100
    {% endif %}
)
SELECT
    a.dim_crm_account_id,

    {% if get_historical_features %} b."event_timestamp"::DATE {% endif %}
    {% if validation %} '2024-05-01'::DATE {% endif %} -- just for validation, hardcore a date
            AS snapshot_month,

    --number of all time features used
    SUM(a.stage_create_alltime_features) AS stage_create_alltime_features_cnt,

FROM base a
{% if get_historical_features %}
INNER JOIN "entity_dataframe" b
    ON a.dim_crm_account_id = b.dim_crm_account_id
    AND a.snapshot_month BETWEEN DATE_TRUNC('month', ADD_MONTHS(b."event_timestamp"::DATE, -6)) AND DATE_TRUNC('month', ADD_MONTHS(b."event_timestamp"::DATE, -1))
{% endif %}
GROUP BY 1, 2
```

Notice how in the first query we need to create a scaffold of all combinations of the entity key (dim_crm_account_id).

In the second query, we can access the `"entity_dataframe"` using the jinja variable `get_historical_features`. This part of the query will only be executed during feature retrieval. This way, we only calculate the transformation at feature retrieval time for the entities and timeframe we care about, speeding the query process. 

We also introduce the `validation` variable. This is because when running `feast apply`, Feast needs to validate that the query can be built. With this we can add logic to make sure that the date key (snapshot_month) is present at validation time (as there is no entity_dataframe at validation time). Also, it let us select only a limited amount of rows in the `base` CTE to make the validation query even faster.

To let feast know it needs to use this jinja workflow you need to add a comment to your SQL query, `-- USE_TEMPLATE_WORKFLOW`

# Implementation details

Changes to make this happen in the codebase are minimal. All the changes in the codebase are commented with `# GITLAB CHANGES` to make it easier to find them.

Since this is a tool used by the Gitlab DS team, we forked the repository to Gitlab, however, this repository still points to the original Github repository so we can keep this up to date with the releases of the Feast package.

This was done with the following steps:

1. git clone https://github.com/feast-dev/feast.git
1. cd feast
1. git remote add gitlab https://gitlab.com/jeanpeguero/feast-gitlab.git
1. git push gitlab master
1. git remote add upstream https://github.com/feast-dev/feast.git

To merge new releases from the main Github repository:

1. git fetch upstream
1. git checkout master
1. git merge upstream/master
1. git push gitlab master

# Building this package

Because this repository lives in Gitlab, we had to translate the Github workflow files to a .gitlab-ci.yml file. We only copied the necessary steps for building the wheels and pushing it to Pypi.

There were some minimal changes performed to the `setup.py` as well. They were done to the how the `version` of the package is generated. Everything else should be the same.

# Publishing changes

To publish changes, first test that they work in testpypi. For this:

1. Create a MR and make changes to the code
1. Run the pipelines manually for building the wheels
1. Run the manual job for publishing to test pipy `upload-to-pypi-test`
1. Test the package

Once you are comfortable with the changes:

1. Create a new tag and release
1. Let the pipelines run to publish the package to pypi
