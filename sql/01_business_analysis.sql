
CREATE TABLE combined_sales (
    transaction_id TEXT,
    customer_id TEXT,
    country TEXT,
    state TEXT,
    city TEXT,
    customer_segment TEXT,
    subscription_plan TEXT,
    billing_cycle TEXT,
    transaction_date DATE,
    transaction_month DATE,
    currency TEXT,
    list_price_local NUMERIC(12,2),
    discount_amount_local NUMERIC(12,2),
    net_revenue_local NUMERIC(12,2),
    payment_status TEXT,
    subscription_event TEXT,
    payment_method TEXT,
    is_new_customer TEXT,
    is_cancelled TEXT,
    data_type TEXT,
    cancellation_flag_mismatch BOOLEAN
);





SELECT
    country,
    COUNT(*) AS total_transactions,
    COUNT(DISTINCT transaction_id) AS unique_transactions
FROM combined_sales
GROUP BY country
ORDER BY country;



SELECT
    country,
    COUNT(*) AS successful_transactions,
    SUM(net_revenue_local) AS successful_revenue
FROM combined_sales
WHERE payment_status = 'Paid'
GROUP BY country
ORDER BY successful_transactions DESC;


SELECT
    country,
    subscription_plan,
    COUNT(*) AS successful_transactions,
    SUM(net_revenue_local) AS total_revenue
FROM combined_sales
WHERE payment_status = 'Paid'
GROUP BY country, subscription_plan
ORDER BY country, total_revenue DESC;



SELECT
    country,
    transaction_month,
    SUM(net_revenue_local) AS monthly_revenue,
    COUNT(*) AS successful_transactions
FROM combined_sales
WHERE payment_status = 'Paid'
GROUP BY country, transaction_month
ORDER BY country, transaction_month;




SELECT
    country,
    COUNT(*) AS total_transactions,
    COUNT(*) FILTER (
        WHERE payment_status = 'Paid'
    ) AS successful_transactions,
    ROUND(
        COUNT(*) FILTER (
            WHERE payment_status = 'Paid'
        ) * 100.0 / COUNT(*),
        2
    ) AS payment_success_rate
FROM combined_sales
GROUP BY country
ORDER BY payment_success_rate DESC;



WITH plan_revenue AS (
    SELECT
        country,
        subscription_plan,
        SUM(net_revenue_local) AS total_revenue
    FROM combined_sales
    WHERE payment_status = 'Paid'
    GROUP BY country, subscription_plan
),
ranked_plans AS (
    SELECT
        country,
        subscription_plan,
        total_revenue,
        RANK() OVER (
            PARTITION BY country
            ORDER BY total_revenue DESC
        ) AS revenue_rank
    FROM plan_revenue
)
SELECT
    country,
    subscription_plan,
    total_revenue,
    revenue_rank
FROM ranked_plans
WHERE revenue_rank = 1
ORDER BY country;




WITH monthly_revenue AS (
    SELECT
        country,
        transaction_month,
        SUM(net_revenue_local) AS monthly_revenue
    FROM combined_sales
    WHERE payment_status = 'Paid'
    GROUP BY country, transaction_month
),
revenue_comparison AS (
    SELECT
        country,
        transaction_month,
        monthly_revenue,
        LAG(monthly_revenue) OVER (
            PARTITION BY country
            ORDER BY transaction_month
        ) AS previous_month_revenue
    FROM monthly_revenue
)
SELECT
    country,
    transaction_month,
    monthly_revenue,
    previous_month_revenue,
    ROUND(
        (
            monthly_revenue - previous_month_revenue
        ) * 100.0 / NULLIF(previous_month_revenue, 0),
        2
    ) AS growth_percentage
FROM revenue_comparison
ORDER BY country, transaction_month;




SELECT
    country,
    COUNT(*) AS cancellation_events,
    COUNT(*) FILTER (
        WHERE payment_status = 'Paid'
    ) AS paid_cancellation_events,
    COUNT(*) FILTER (
        WHERE payment_status = 'Failed'
    ) AS failed_cancellation_events,
    COUNT(*) FILTER (
        WHERE payment_status = 'Refunded'
    ) AS refunded_cancellation_events
FROM combined_sales
WHERE subscription_event = 'Cancellation'
GROUP BY country
ORDER BY country;



SELECT
    country,
    customer_segment,
    COUNT(*) AS successful_transactions,
    SUM(net_revenue_local) AS total_revenue,
    ROUND(AVG(net_revenue_local), 2) AS average_transaction_value
FROM combined_sales
WHERE payment_status = 'Paid'
GROUP BY country, customer_segment
ORDER BY country, total_revenue DESC;



SELECT
    country,
    customer_segment,
    COUNT(*) AS successful_transactions,
    SUM(net_revenue_local) AS total_revenue,
    ROUND(AVG(net_revenue_local), 2) AS average_transaction_value
FROM combined_sales
WHERE payment_status = 'Paid'
GROUP BY country, customer_segment
ORDER BY country, total_revenue DESC;



WITH customer_transactions AS (
    SELECT
        country,
        customer_id,
        COUNT(*) AS successful_transactions,
        SUM(net_revenue_local) AS customer_revenue
    FROM combined_sales
    WHERE payment_status = 'Paid'
    GROUP BY country, customer_id
)
SELECT
    country,
    COUNT(*) AS customers_with_successful_payments,
    COUNT(*) FILTER (
        WHERE successful_transactions > 1
    ) AS repeat_customers,
    ROUND(
        COUNT(*) FILTER (
            WHERE successful_transactions > 1
        ) * 100.0 / COUNT(*),
        2
    ) AS repeat_customer_percentage,
    ROUND(AVG(customer_revenue), 2) AS average_customer_revenue
FROM customer_transactions
GROUP BY country
ORDER BY country;




SELECT
    country,
    COUNT(*) AS total_transactions,
    COUNT(*) FILTER (
        WHERE payment_status = 'Refunded'
    ) AS refunded_transactions,
    ROUND(
        COUNT(*) FILTER (
            WHERE payment_status = 'Refunded'
        ) * 100.0 / COUNT(*),
        2
    ) AS refund_rate_percentage
FROM combined_sales
GROUP BY country
ORDER BY refund_rate_percentage DESC;


SELECT
    country,
    COUNT(*) AS total_transactions,
    COUNT(*) FILTER (
        WHERE is_new_customer = 'Yes'
    ) AS new_customer_transactions,
    COUNT(*) FILTER (
        WHERE is_new_customer = 'No'
    ) AS existing_customer_transactions,
    ROUND(
        COUNT(*) FILTER (
            WHERE is_new_customer = 'Yes'
        ) * 100.0 / COUNT(*),
        2
    ) AS new_customer_percentage
FROM combined_sales
GROUP BY country
ORDER BY country;


WITH city_revenue AS (
    SELECT
        country,
        city,
        SUM(net_revenue_local) AS total_revenue,
        COUNT(*) AS successful_transactions
    FROM combined_sales
    WHERE payment_status = 'Paid'
    GROUP BY country, city
),
ranked_cities AS (
    SELECT
        country,
        city,
        total_revenue,
        successful_transactions,
        DENSE_RANK() OVER (
            PARTITION BY country
            ORDER BY total_revenue DESC
        ) AS revenue_rank
    FROM city_revenue
)
SELECT
    country,
    city,
    total_revenue,
    successful_transactions,
    revenue_rank
FROM ranked_cities
WHERE revenue_rank <= 3
ORDER BY country, revenue_rank;




SELECT
    country,
    payment_method,
    COUNT(*) AS successful_transactions,
    SUM(net_revenue_local) AS total_revenue
FROM combined_sales
WHERE payment_status = 'Paid'
GROUP BY country, payment_method
ORDER BY country, successful_transactions DESC;



SELECT
    country,
    subscription_plan,
    COUNT(*) AS successful_transactions,
    ROUND(AVG(net_revenue_local), 2) AS average_transaction_value
FROM combined_sales
WHERE payment_status = 'Paid'
GROUP BY country, subscription_plan
ORDER BY country, average_transaction_value DESC;



SELECT
    country,
    subscription_plan,
    COUNT(*) AS total_transactions,
    COUNT(*) FILTER (
        WHERE payment_status = 'Failed'
    ) AS failed_transactions,
    ROUND(
        COUNT(*) FILTER (
            WHERE payment_status = 'Failed'
        ) * 100.0 / COUNT(*),
        2
    ) AS failure_rate_percentage
FROM combined_sales
GROUP BY country, subscription_plan
ORDER BY country, failure_rate_percentage DESC;


SELECT
    country,
    customer_id,
    COUNT(*) AS successful_transactions,
    SUM(net_revenue_local) AS total_revenue
FROM combined_sales
WHERE payment_status = 'Paid'
GROUP BY country, customer_id
ORDER BY total_revenue DESC
LIMIT 5;


WITH customer_revenue AS (
    SELECT
        country,
        customer_id,
        COUNT(*) AS successful_transactions,
        SUM(net_revenue_local) AS total_revenue
    FROM combined_sales
    WHERE payment_status = 'Paid'
    GROUP BY country, customer_id
),
ranked_customers AS (
    SELECT
        country,
        customer_id,
        successful_transactions,
        total_revenue,
        DENSE_RANK() OVER (
            PARTITION BY country
            ORDER BY total_revenue DESC
        ) AS revenue_rank
    FROM customer_revenue
)
SELECT
    country,
    customer_id,
    successful_transactions,
    total_revenue,
    revenue_rank
FROM ranked_customers
WHERE revenue_rank <= 3
ORDER BY country, revenue_rank;




SELECT
    country,
    COUNT(*) AS total_transactions,
    COUNT(*) FILTER (
        WHERE subscription_event = 'Cancellation'
    ) AS cancellation_events,
    ROUND(
        COUNT(*) FILTER (
            WHERE subscription_event = 'Cancellation'
        ) * 100.0 / COUNT(*),
        2
    ) AS cancellation_event_rate_percentage
FROM combined_sales
GROUP BY country
ORDER BY country;



SELECT
    country,
    billing_cycle,
    COUNT(*) AS successful_transactions,
    SUM(net_revenue_local) AS total_revenue,
    ROUND(AVG(net_revenue_local), 2) AS average_transaction_value
FROM combined_sales
WHERE payment_status = 'Paid'
GROUP BY country, billing_cycle
ORDER BY country, total_revenue DESC;



SELECT
    country,
    transaction_month,
    subscription_plan,
    COUNT(*) AS successful_transactions,
    SUM(net_revenue_local) AS total_revenue
FROM combined_sales
WHERE payment_status = 'Paid'
GROUP BY
    country,
    transaction_month,
    subscription_plan
ORDER BY
    country,
    transaction_month,
    total_revenue DESC;


WITH customer_revenue AS (
    SELECT
        country,
        customer_id,
        SUM(net_revenue_local) AS total_customer_revenue
    FROM combined_sales
    WHERE payment_status = 'Paid'
    GROUP BY country, customer_id
)
SELECT
    country,
    COUNT(*) AS paying_customers,
    ROUND(AVG(total_customer_revenue), 2) AS average_revenue_per_customer
FROM customer_revenue
GROUP BY country
ORDER BY country;


WITH monthly_plan_revenue AS (
    SELECT
        country,
        transaction_month,
        subscription_plan,
        SUM(net_revenue_local) AS total_revenue
    FROM combined_sales
    WHERE payment_status = 'Paid'
    GROUP BY
        country,
        transaction_month,
        subscription_plan
),
ranked_plans AS (
    SELECT
        country,
        transaction_month,
        subscription_plan,
        total_revenue,
        ROW_NUMBER() OVER (
            PARTITION BY country, transaction_month
            ORDER BY total_revenue DESC, subscription_plan
        ) AS plan_rank
    FROM monthly_plan_revenue
)
SELECT
    country,
    transaction_month,
    subscription_plan,
    total_revenue
FROM ranked_plans
WHERE plan_rank = 1
ORDER BY country, transaction_month;




SELECT
    country,
    subscription_plan,
    COUNT(*) FILTER (
        WHERE payment_status = 'Paid'
    ) AS successful_transactions,
    COUNT(*) FILTER (
        WHERE payment_status = 'Failed'
    ) AS failed_transactions,
    ROUND(
        COUNT(*) FILTER (
            WHERE payment_status = 'Failed'
        ) * 100.0 / NULLIF(COUNT(*), 0),
        2
    ) AS failed_payment_percentage
FROM combined_sales
GROUP BY country, subscription_plan
ORDER BY country, failed_payment_percentage DESC;



SELECT
    country,
    payment_status,
    COUNT(*) AS transaction_count,
    SUM(net_revenue_local) AS total_net_revenue,
    ROUND(AVG(net_revenue_local), 2) AS average_net_revenue
FROM combined_sales
GROUP BY country, payment_status
ORDER BY country, payment_status;


WITH monthly_revenue AS (
    SELECT
        country,
        transaction_month,
        SUM(net_revenue_local) AS monthly_revenue
    FROM combined_sales
    WHERE payment_status = 'Paid'
    GROUP BY country, transaction_month
)
SELECT
    country,
    transaction_month,
    monthly_revenue,
    LAG(monthly_revenue) OVER (
        PARTITION BY country
        ORDER BY transaction_month
    ) AS previous_month_revenue,
    ROUND(
        monthly_revenue - LAG(monthly_revenue) OVER (
            PARTITION BY country
            ORDER BY transaction_month
        ),
        2
    ) AS revenue_change
FROM monthly_revenue
ORDER BY country, transaction_month;


SELECT
    country,
    customer_id,
    COUNT(*) FILTER (
        WHERE subscription_event = 'Cancellation'
    ) AS cancellation_events,
    COUNT(*) FILTER (
        WHERE payment_status = 'Paid'
    ) AS successful_transactions,
    SUM(net_revenue_local) FILTER (
        WHERE payment_status = 'Paid'
    ) AS successful_revenue
FROM combined_sales
GROUP BY country, customer_id
HAVING COUNT(*) FILTER (
    WHERE subscription_event = 'Cancellation'
) > 0
ORDER BY cancellation_events DESC,
         successful_revenue DESC NULLS LAST;



SELECT
    country,
    customer_segment,
    COUNT(*) AS total_transactions,
    COUNT(*) FILTER (
        WHERE payment_status = 'Paid'
    ) AS successful_transactions,
    SUM(net_revenue_local) FILTER (
        WHERE payment_status = 'Paid'
    ) AS successful_revenue,
    ROUND(
        AVG(net_revenue_local) FILTER (
            WHERE payment_status = 'Paid'
        ),
        2
    ) AS average_successful_transaction
FROM combined_sales
GROUP BY country, customer_segment
ORDER BY country, successful_revenue DESC;



SELECT
    country,
    transaction_month,
    COUNT(*) AS total_transactions,
    COUNT(*) FILTER (
        WHERE payment_status = 'Paid'
    ) AS successful_transactions,
    COUNT(*) FILTER (
        WHERE payment_status = 'Failed'
    ) AS failed_transactions,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE payment_status = 'Paid'
        ) / NULLIF(
            COUNT(*) FILTER (
                WHERE payment_status IN ('Paid', 'Failed')
            ), 0
        ),
        2
    ) AS payment_success_rate
FROM combined_sales
GROUP BY country, transaction_month
ORDER BY country, transaction_month;


SELECT
    country,
    COUNT(*) AS total_transactions,

    COUNT(*) FILTER (
        WHERE payment_status = 'Paid'
    ) AS successful_transactions,

    COUNT(*) FILTER (
        WHERE payment_status = 'Failed'
    ) AS failed_transactions,

    COUNT(*) FILTER (
        WHERE payment_status = 'Refunded'
    ) AS refunded_transactions,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE payment_status = 'Paid'
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS paid_transaction_percentage,

    ROUND(
        SUM(net_revenue_local) FILTER (
            WHERE payment_status = 'Paid'
        ),
        2
    ) AS successful_revenue,

    ROUND(
        AVG(net_revenue_local) FILTER (
            WHERE payment_status = 'Paid'
        ),
        2
    ) AS average_paid_transaction_value

FROM combined_sales
GROUP BY country
ORDER BY country;
WITH monthly_revenue AS (
    SELECT
        country,
        transaction_month,
        SUM(net_revenue_local) AS monthly_revenue
    FROM combined_sales
    WHERE payment_status = 'Paid'
    GROUP BY country, transaction_month
),
revenue_comparison AS (
    SELECT
        country,
        transaction_month,
        monthly_revenue,
        LAG(monthly_revenue) OVER (
            PARTITION BY country
            ORDER BY transaction_month
        ) AS previous_month_revenue
    FROM monthly_revenue
)
SELECT
    country,
    transaction_month,
    ROUND(monthly_revenue, 2) AS monthly_revenue,
    ROUND(previous_month_revenue, 2) AS previous_month_revenue,
    ROUND(
        100.0 * (monthly_revenue - previous_month_revenue)
        / NULLIF(previous_month_revenue, 0),
        2
    ) AS revenue_growth_percentage
FROM revenue_comparison
ORDER BY country, transaction_month;