--
-- PostgreSQL database dump
--

-- Dumped from database version 15.1


SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 241 (class 1259 OID 16590)
-- Name: vt_avgreviewbydelivertime; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vt_avgreviewbydelivertime AS
 SELECT avg((o.order_delivered_customer_date - o.order_purchase_timestamp)) AS avgdeliverytime,
    avg(or2.review_score) AS score
   FROM ((((public.orders o
     JOIN public.customers c ON (((c.customer_id)::text = (o.customer_id)::text)))
     JOIN public.order_items oi ON (((oi.order_id)::text = (o.order_id)::text)))
     JOIN public.sellers s ON (((s.seller_id)::text = (oi.seller_id)::text)))
     LEFT JOIN public.order_reviews or2 ON (((o.order_id)::text = (or2.order_id)::text)))
  WHERE ((s.seller_state)::text = (c.customer_state)::text);


ALTER TABLE public.vt_avgreviewbydelivertime OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 16595)
-- Name: vt_avgreviewbystate; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vt_avgreviewbystate AS
 SELECT c.customer_state,
    s.seller_state,
    avg(or2.review_score) AS avgreview
   FROM ((((public.orders o
     JOIN public.customers c ON (((c.customer_id)::text = (o.customer_id)::text)))
     JOIN public.order_items oi ON (((oi.order_id)::text = (o.order_id)::text)))
     JOIN public.sellers s ON (((s.seller_id)::text = (oi.seller_id)::text)))
     LEFT JOIN public.order_reviews or2 ON (((o.order_id)::text = (or2.order_id)::text)))
  GROUP BY c.customer_state, s.seller_state;


ALTER TABLE public.vt_avgreviewbystate OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 16561)
-- Name: vt_avgtimetodeliver; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vt_avgtimetodeliver AS
 select count(o.order_delivered_customer_date),avg(o.order_estimated_delivery_date-o.order_delivered_customer_date),count(o.order_delivered_customer_date)::FLOAT/(select count(order_delivered_customer_date) from orders)::FLOAT as percentimpact 
from 
orders o  
where 
o.order_estimated_delivery_date < o.order_delivered_customer_date ;


ALTER TABLE public.vt_avgtimetodeliver OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 16566)
-- Name: vt_avgtimetodeliverbtstates; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vt_avgtimetodeliverbtstates AS
 SELECT s.seller_state AS sstate,
    c.customer_state AS cstate,
    avg((o.order_delivered_customer_date - o.order_purchase_timestamp)) AS avgdeliverytime
   FROM (((public.orders o
     JOIN public.customers c ON (((c.customer_id)::text = (o.customer_id)::text)))
     JOIN public.order_items oi ON (((oi.order_id)::text = (o.order_id)::text)))
     JOIN public.sellers s ON (((s.seller_id)::text = (oi.seller_id)::text)))
  WHERE ((s.seller_state)::text != (c.customer_state)::text)
  GROUP BY s.seller_state, c.customer_state;


ALTER TABLE public.vt_avgtimetodeliverbtstates OWNER TO postgres;

--
-- TOC entry 240 (class 1259 OID 16585)
-- Name: vt_avgtimetodelivervsreviewdiffstate; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vt_avgtimetodelivervsreviewdiffstate AS
 SELECT avg((o.order_delivered_customer_date - o.order_purchase_timestamp)) AS avgdeliverytime,
    avg(or2.review_score) AS score
   FROM ((((public.orders o
     JOIN public.customers c ON (((c.customer_id)::text = (o.customer_id)::text)))
     JOIN public.order_items oi ON (((oi.order_id)::text = (o.order_id)::text)))
     JOIN public.sellers s ON (((s.seller_id)::text = (oi.seller_id)::text)))
     LEFT JOIN public.order_reviews or2 ON (((o.order_id)::text = (or2.order_id)::text)))
  WHERE ((s.seller_state)::text <> (c.customer_state)::text);


ALTER TABLE public.vt_avgtimetodelivervsreviewdiffstate OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 16580)
-- Name: vt_avgtimetodelivervsreviewsamestate; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vt_avgtimetodelivervsreviewsamestate AS
 SELECT s.seller_state AS sstate,
    c.customer_state AS cstate,
    avg((o.order_delivered_customer_date - o.order_purchase_timestamp)) AS avgdeliverytime,
    avg(or2.review_score) AS avg
   FROM ((((public.orders o
     JOIN public.customers c ON (((c.customer_id)::text = (o.customer_id)::text)))
     JOIN public.order_items oi ON (((oi.order_id)::text = (o.order_id)::text)))
     JOIN public.sellers s ON (((s.seller_id)::text = (oi.seller_id)::text)))
     LEFT JOIN public.order_reviews or2 ON (((o.order_id)::text = (or2.order_id)::text)))
  WHERE ((s.seller_state)::text = (c.customer_state)::text)
  GROUP BY s.seller_state, c.customer_state;


ALTER TABLE public.vt_avgtimetodelivervsreviewsamestate OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 16517)
-- Name: vt_buysbycity; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vt_buysbycity AS
 SELECT c.customer_city AS city,
    count(o.order_id) AS noforders
   FROM (public.customers c
     JOIN public.orders o ON (((o.customer_id)::text = (c.customer_id)::text)))
  GROUP BY c.customer_city
  ORDER BY (count(o.order_id)) DESC;


ALTER TABLE public.vt_buysbycity OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16513)
-- Name: vt_buysbystate; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vt_buysbystate AS
 SELECT c.customer_state AS state,
    count(o.order_id) AS noforders
   FROM (public.customers c
     JOIN public.orders o ON (((o.customer_id)::text = (c.customer_id)::text)))
  GROUP BY c.customer_state
  ORDER BY (count(o.order_id)) DESC;


ALTER TABLE public.vt_buysbystate OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16531)
-- Name: vt_itembyorderbystate; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vt_itembyorderbystate AS
 SELECT c.customer_state AS state,
    ((count(oi.order_id))::double precision / (count(DISTINCT oi.order_id))::double precision) AS noforders
   FROM ((public.customers c
     JOIN public.orders o ON (((o.customer_id)::text = (c.customer_id)::text)))
     JOIN public.order_items oi ON (((o.order_id)::text = (oi.order_id)::text)))
  GROUP BY c.customer_state
  ORDER BY ((count(oi.order_id))::double precision / (count(DISTINCT oi.order_id))::double precision) DESC;


ALTER TABLE public.vt_itembyorderbystate OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16541)
-- Name: vt_itemnamesellbystate; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vt_itemnamesellbystate AS
 SELECT s.seller_state,
    p.product_category_name,
    count(oi.order_id) AS nofsales,
    ( SELECT count(oi_1.order_id) AS totalofsales
           FROM (public.order_items oi_1
             JOIN public.sellers a ON (((oi_1.seller_id)::text = (a.seller_id)::text)))
          WHERE ((a.seller_state)::text = (s.seller_state)::text)) AS totalofsales
   FROM ((public.products p
     JOIN public.order_items oi ON (((oi.product_id)::text = (p.product_id)::text)))
     JOIN public.sellers s ON (((s.seller_id)::text = (oi.seller_id)::text)))
  GROUP BY p.product_category_name, s.seller_state
  ORDER BY s.seller_state, (count(oi.order_id)) DESC;


ALTER TABLE public.vt_itemnamesellbystate OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 16536)
-- Name: vt_itemsbyorderbystate; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vt_itemsbyorderbystate AS
 SELECT c.customer_state AS state,
    ((count(oi.order_id))::double precision / (count(DISTINCT oi.order_id))::double precision) AS noforders
   FROM ((public.customers c
     JOIN public.orders o ON (((o.customer_id)::text = (c.customer_id)::text)))
     JOIN public.order_items oi ON (((o.order_id)::text = (oi.order_id)::text)))
  GROUP BY c.customer_state;


ALTER TABLE public.vt_itemsbyorderbystate OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16503)
-- Name: vt_paymentsbycity; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vt_paymentsbycity AS
 SELECT op.payment_type AS paymenttype,
    c.customer_city AS city,
    count(o.order_id) AS noforders
   FROM ((public.customers c
     JOIN public.orders o ON (((o.customer_id)::text = (c.customer_id)::text)))
     JOIN public.order_payments op ON (((op.order_id)::text = (o.order_id)::text)))
  GROUP BY op.payment_type, c.customer_city;


ALTER TABLE public.vt_paymentsbycity OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16508)
-- Name: vt_paymentsbystate; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vt_paymentsbystate AS
 SELECT op.payment_type AS paymenttype,
    c.customer_state AS state,
    count(o.order_id) AS noforders
   FROM ((public.customers c
     JOIN public.orders o ON (((o.customer_id)::text = (c.customer_id)::text)))
     JOIN public.order_payments op ON (((op.order_id)::text = (o.order_id)::text)))
  GROUP BY op.payment_type, c.customer_state
  ORDER BY c.customer_state, (count(o.order_id)) DESC;


ALTER TABLE public.vt_paymentsbystate OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 16551)
-- Name: vt_reviewbyprice; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vt_reviewbyprice AS
 SELECT p.product_category_name,
    avg(or2.review_score) AS score,
    ( SELECT (count(order_items.price) + count(order_items.freight_value)) AS avg_totalcost
           FROM (public.order_items
             JOIN public.products p2 ON (((p2.product_id)::text = (order_items.product_id)::text)))
          WHERE ((p2.product_category_name)::text = (p.product_category_name)::text)) AS avg_totalcost
   FROM ((public.products p
     JOIN public.order_items oi ON (((p.product_id)::text = (oi.product_id)::text)))
     JOIN public.order_reviews or2 ON (((or2.order_id)::text = (oi.order_id)::text)))
  GROUP BY p.product_category_name
  ORDER BY (avg(or2.review_score)), ( SELECT (count(order_items.price) + count(order_items.freight_value)) AS avg_totalcost
           FROM (public.order_items
             JOIN public.products p2 ON (((p2.product_id)::text = (order_items.product_id)::text)))
          WHERE ((p2.product_category_name)::text = (p.product_category_name)::text)) DESC;


ALTER TABLE public.vt_reviewbyprice OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 16546)
-- Name: vt_reviewbyproduct; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vt_reviewbyproduct AS
 SELECT p.product_category_name,
    avg(or2.review_score) AS score
   FROM ((public.products p
     JOIN public.order_items oi ON (((p.product_id)::text = (oi.product_id)::text)))
     JOIN public.order_reviews or2 ON (((or2.order_id)::text = (oi.order_id)::text)))
  GROUP BY p.product_category_name
  ORDER BY (avg(or2.review_score)) DESC;


ALTER TABLE public.vt_reviewbyproduct OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 16526)
-- Name: vt_salesbycity; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vt_salesbycity AS
 SELECT s.seller_city AS city,
    count(o.order_id) AS noforders
   FROM ((public.sellers s
     JOIN public.order_items oi ON (((oi.seller_id)::text = (s.seller_id)::text)))
     JOIN public.orders o ON (((oi.order_id)::text = (o.order_id)::text)))
  GROUP BY s.seller_city
  ORDER BY (count(o.order_id)) DESC;


ALTER TABLE public.vt_salesbycity OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16521)
-- Name: vt_salesbystate; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vt_salesbystate AS
 SELECT s.seller_state AS state,
    count(o.order_id) AS noforders
   FROM ((public.sellers s
     JOIN public.order_items oi ON (((oi.seller_id)::text = (s.seller_id)::text)))
     JOIN public.orders o ON (((oi.order_id)::text = (o.order_id)::text)))
  GROUP BY s.seller_state
  ORDER BY (count(o.order_id)) DESC;


ALTER TABLE public.vt_salesbystate OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 16556)
-- Name: vt_sellerreviews; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vt_sellerreviews AS
 SELECT s.seller_id,
    avg(or2.review_score) AS avg_reviews,
    count(or2.review_score) AS nofreviews
   FROM ((public.sellers s
     JOIN public.order_items oi ON (((oi.seller_id)::text = (s.seller_id)::text)))
     JOIN public.order_reviews or2 ON (((or2.order_id)::text = (oi.order_id)::text)))
  GROUP BY s.seller_id
  ORDER BY (avg(or2.review_score)) DESC;


ALTER TABLE public.vt_sellerreviews OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16495)
-- Name: vt_timesdeliveredlate; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vt_timesdeliveredlate AS
 SELECT o.order_status,
    count(o.order_status) AS orderoverestimated,
    ( SELECT count(orders.*) AS count
           FROM public.orders) AS numberoforders
   FROM public.orders o
  WHERE (o.order_estimated_delivery_date < o.order_delivered_customer_date)
  GROUP BY o.order_status;


ALTER TABLE public.vt_timesdeliveredlate OWNER TO postgres;

--
-- TOC entry 238 (class 1259 OID 16575)
-- Name: vt_timeslateavgtimetodeliver; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vt_timeslateavgtimetodeliver AS
 SELECT s.seller_state AS sstate,
    c.customer_state AS cstate,
    avg((o.order_delivered_customer_date - o.order_purchase_timestamp)) AS avgdeliverytime,
    avg(or2.review_score) AS avg
   FROM ((((public.orders o
     JOIN public.customers c ON (((c.customer_id)::text = (o.customer_id)::text)))
     JOIN public.order_items oi ON (((oi.order_id)::text = (o.order_id)::text)))
     JOIN public.sellers s ON (((s.seller_id)::text = (oi.seller_id)::text)))
     LEFT JOIN public.order_reviews or2 ON (((o.order_id)::text = (or2.order_id)::text)))
  WHERE ((s.seller_state)::text = (c.customer_state)::text)
  GROUP BY s.seller_state, c.customer_state;


ALTER TABLE public.vt_timeslateavgtimetodeliver OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 16571)
-- Name: vt_totalavgtimetodeliver; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vt_totalavgtimetodeliver AS
 SELECT count(o.order_delivered_customer_date) AS count,
    avg((o.order_estimated_delivery_date - o.order_delivered_customer_date)) AS avg,
    ((count(o.order_delivered_customer_date))::double precision / (( SELECT count(orders.order_delivered_customer_date) AS count
           FROM public.orders))::double precision) AS percentimpact
   FROM public.orders o
  WHERE (o.order_estimated_delivery_date < o.order_delivered_customer_date);


ALTER TABLE public.vt_totalavgtimetodeliver OWNER TO postgres;

-- Completed on 2022-12-06 10:48:13

--
-- PostgreSQL database dump complete
--

