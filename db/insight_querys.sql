
-- orders that has been delivered over the estimated time
select order_status,count(order_status) as OrderOverEstimated,(select count(orders) from orders  ) as NumberOfOrders
from orders o 
where 
order_estimated_delivery_date < order_delivered_customer_date 
group by order_status



-- top payment methods by city 

select op.payment_type PaymentType,c.customer_city city,count(o.order_id) NofOrders 
from
customers c 
inner join
orders o 
on o.customer_id = c.customer_id 
inner join 
order_payments op 
on op.order_id = o.order_id 
group by  op.payment_type,c.customer_city
order by city ,NofOrders desc 

-- top payment methods by State 

select op.payment_type PaymentType,c.customer_state  state,count(o.order_id) NofOrders 
from
customers c 
inner join
orders o 
on o.customer_id = c.customer_id 
inner join 
order_payments op 
on op.order_id = o.order_id 
group by  op.payment_type,c.customer_state
order by state ,NofOrders desc 

-- top buys by state 

select c.customer_state  state,count(o.order_id) NofOrders 
from
customers c 
inner join
orders o 
on o.customer_id = c.customer_id 
group by  c.customer_state
order by NofOrders desc 

-- top buys by City
select c.customer_state  state,count(o.order_id) NofOrders 
from
customers c 
inner join
orders o 
on o.customer_id = c.customer_id 
group by  c.customer_state
order by NofOrders desc 


-- top Sales by State

select s.seller_state  state,count(o.order_id) NofOrders 
from
sellers s  
inner join
order_items oi  
on oi.seller_id = s.seller_id 
inner join 
orders o 
on oi.order_id = o.order_id 
group by  s.seller_state
order by NofOrders desc 


-- top Sales by City

select s.seller_city  city,count(o.order_id) NofOrders 
from
sellers s  
inner join
order_items oi  
on oi.seller_id = s.seller_id 
inner join 
orders o 
on oi.order_id = o.order_id 
group by  s.seller_city
order by NofOrders desc 


-- avg of items by order by State

select c.customer_state  state,( cast( count(oi.order_id) as FLOAT ) / cast( count( distinct(oi.order_id)) as FLOAT))  NofOrders
from
customers c   
inner join
orders o 
on o.customer_id = c.customer_id  
inner join 
order_items oi  
on  o.order_id = oi.order_id
group by  c.customer_state
order by NofOrders desc 


-- top sell products by state
select s.seller_state,p.product_category_name, count(oi.order_id) NofSales,
(
select count(oi.order_id) TotalofSales 
from
order_items oi
inner join
sellers a  
on oi.seller_id = a.seller_id 

where a.seller_state = s.seller_state
)





-- avg review by product

select p.product_category_name, avg(or2.review_score) as score
from
products p 
inner join 
order_items oi 
on
p.product_id = oi.product_id 
inner join 
order_reviews or2
on
or2.order_id = oi.order_id 

group by p.product_category_name
order by score desc


-- avg review by product/price

select p.product_category_name, avg(or2.review_score) as score,
( select count(price)+count(freight_value) as avg_totalcost
	from order_items
		inner join
			products p2
				on p2.product_id = order_items.product_id
					where p2.product_category_name  = p.product_category_name )
					
from
products p 
inner join 
order_items oi 
on
p.product_id = oi.product_id 
inner join 
order_reviews or2
on
or2.order_id = oi.order_id 

group by p.product_category_name
order by score,avg_totalcost desc


-- Sellers reviews vs number of reviews
select s.seller_id, avg(or2.review_score) as avg_reviews,count(or2.review_score) as nofreviews

from
sellers s
inner join
order_items oi 
on 
oi.seller_id = s.seller_id 
inner join order_reviews or2 
on or2.order_id = oi.order_id 
group by s.seller_id 
order by avg_reviews DESC

-- Avg time to deliver
select s.seller_state as sstate,c.customer_state as cstate ,avg(o.order_delivered_customer_date - o.order_purchase_timestamp) as avgdeliverytime
from
orders o
inner join 
customers c 
on
c.customer_id = o.customer_id 
inner join
order_items oi 
on
oi.order_id = o.order_id 
inner join 
sellers s 
on
s.seller_id = oi.seller_id 
group by s.seller_state , c.customer_state 

-- Avg time to deliver between the same state

-- Avg time to deliver
select s.seller_state as sstate,c.customer_state as cstate ,avg(o.order_delivered_customer_date - o.order_purchase_timestamp) as avgdeliverytime
from
orders o
inner join 
customers c 
on
c.customer_id = o.customer_id 
inner join
order_items oi 
on
oi.order_id = o.order_id 
inner join 
sellers s 
on
s.seller_id = oi.seller_id 
where s.seller_state  = c.customer_state 
group by s.seller_state , c.customer_state 


-- times and avg time that the delivery time was over the delivery estimated time 
select count(o.order_delivered_customer_date),avg(o.order_estimated_delivery_date-o.order_delivered_customer_date),count(o.order_delivered_customer_date)::FLOAT/(select count(order_delivered_customer_date) from orders)::FLOAT as percentimpact
from
orders o 
where 
o.order_estimated_delivery_date < o.order_delivered_customer_date









-- Avg review vs time to delivery in the same state

select s.seller_state as sstate,c.customer_state as cstate ,avg(o.order_delivered_customer_date - o.order_purchase_timestamp) as avgdeliverytime,avg(or2.review_score)
from
orders o
inner join 
customers c 
on
c.customer_id = o.customer_id 
inner join
order_items oi 
on
oi.order_id = o.order_id 
inner join 
sellers s 
on
s.seller_id = oi.seller_id 
left join 
order_reviews or2 
on
o.order_id = or2.order_id 

where s.seller_state  = c.customer_state 
group by s.seller_state , c.customer_state 



-- Avg review vs time to delivery between different state

select s.seller_state as sstate,c.customer_state as cstate ,avg(o.order_delivered_customer_date - o.order_purchase_timestamp) as avgdeliverytime,avg(or2.review_score)
from
orders o
inner join 
customers c 
on
c.customer_id = o.customer_id 
inner join
order_items oi 
on
oi.order_id = o.order_id 
inner join 
sellers s 
on
s.seller_id = oi.seller_id 
left join 
order_reviews or2 
on
o.order_id = or2.order_id 

where s.seller_state  != c.customer_state 
group by s.seller_state , c.customer_state 



-- Avg review by time to delivery in total


select avg(o.order_delivered_customer_date - o.order_purchase_timestamp) as avgdeliverytime,avg(or2.review_score) score
from
orders o
inner join 
customers c 
on
c.customer_id = o.customer_id 
inner join
order_items oi 
on
oi.order_id = o.order_id 
inner join 
sellers s 
on
s.seller_id = oi.seller_id 
left join 
order_reviews or2 
on
o.order_id = or2.order_id 

where s.seller_state  != c.customer_state 
 
select avg(o.order_delivered_customer_date - o.order_purchase_timestamp) as avgdeliverytime,avg(or2.review_score) score
from
orders o
inner join 
customers c 
on
c.customer_id = o.customer_id 
inner join
order_items oi 
on
oi.order_id = o.order_id 
inner join 
sellers s 
on
s.seller_id = oi.seller_id 
left join 
order_reviews or2 
on
o.order_id = or2.order_id 

where s.seller_state  = c.customer_state 



-- avg review in state for buyers and sellers

select c.customer_state,s.seller_state,avg(or2.review_score) as avgreview
from
orders o
inner join 
customers c 
on
c.customer_id = o.customer_id 
inner join
order_items oi 
on
oi.order_id = o.order_id 
inner join 
sellers s 
on
s.seller_id = oi.seller_id 
left join 
order_reviews or2 
on
o.order_id = or2.order_id 

group by c.customer_state,s.seller_state


-- avg review in state for buyers

select c.customer_state,avg(or2.review_score) as avgreview
from
orders o
inner join 
customers c 
on
c.customer_id = o.customer_id 
inner join
order_items oi 
on
oi.order_id = o.order_id 
inner join 
sellers s 
on
s.seller_id = oi.seller_id 
left join 
order_reviews or2 
on
o.order_id = or2.order_id 

group by c.customer_state



-- avg review in state for sellers

select s.seller_state,avg(or2.review_score) as avgreview
from
orders o
inner join 
customers c 
on
c.customer_id = o.customer_id 
inner join
order_items oi 
on
oi.order_id = o.order_id 
inner join 
sellers s 
on
s.seller_id = oi.seller_id 
left join 
order_reviews or2 
on
o.order_id = or2.order_id 

group by s.seller_state