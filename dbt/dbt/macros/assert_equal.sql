{% macro test_equality(model) %} -- macro definition

{% set compare_model = kwargs.get('compare_model') %} -- get compare_model input parameter
{% set env = kwargs.get('env') %} -- get env input parameter

{%- if target.name == env -%} -- check if env input parameter matches the current environment

SELECT count(*) 
FROM (
        (SELECT * FROM {{ model }} except SELECT * FROM {{ compare_model }} )  
        UNION 
        (SELECT * FROM {{ compare_model }} except SELECT * FROM {{ model }} )
) tmp

{%- else -%}

SELECT 0 -- if no input or different env return true

{%- endif -%}

{% endmacro %}