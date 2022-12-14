
-- PostgreSQL database dump
-- Dumped from database version 15.1

-- Database: DB_company

-- DROP DATABASE IF EXISTS "DB_company";

CREATE DATABASE "DB_company"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Spanish_Argentina.1252'
    LC_CTYPE = 'Spanish_Argentina.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;


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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: CUSTOMER; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."customers" (
    customer_id character varying(32) NOT NULL,
    customer_zip_code_prefix integer NOT NULL,
    customer_city character varying(32) NOT NULL,
    customer_state character varying(2) NOT NULL
);


ALTER TABLE public."customers" OWNER TO postgres;

--
-- Name: GEOLOCATION; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."geolocation" (
    geolocation_zip_code_prefix integer NOT NULL,
    geolocation_lat double precision NOT NULL,
    geolocation_lng double precision NOT NULL,
    geolocation_city character varying(38) NOT NULL,
    geolocation_state character varying(2) NOT NULL
);


ALTER TABLE public."geolocation" OWNER TO postgres;

--
-- Name: ORDERS; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."orders" (
    order_id character varying(32) NOT NULL,
    customer_id character varying(32) NOT NULL,
    order_status character varying(11) NOT NULL,
    order_purchase_timestamp timestamp without time zone,
    order_approved_at timestamp without time zone,
    order_delivered_carrier_date timestamp without time zone,
    order_delivered_customer_date timestamp without time zone,
    order_estimated_delivery_date timestamp without time zone
);


ALTER TABLE public."orders" OWNER TO postgres;

--
-- Name: ORDER_ITEMS; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."order_items" (
    order_id character varying(32) NOT NULL,
    product_id character varying(32) NOT NULL,
    seller_id character varying(32) NOT NULL,
    shipping_limit_date timestamp without time zone,
    price real NOT NULL,
    freight_value real
);


ALTER TABLE public."order_items" OWNER TO postgres;

--
-- Name: ORDER_PAYMENTS; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."order_payments" (
    order_id character varying(32) NOT NULL,
    payment_type character varying(32) NOT NULL,
    payment_installments smallint,
    payment_value real NOT NULL
);


ALTER TABLE public."order_payments" OWNER TO postgres;

--
-- Name: ORDER_REVIEWS; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."order_reviews" (
    review_id character varying(32) NOT NULL,
    order_id character varying(32) NOT NULL,
    review_score smallint,
    review_comment_message character varying(208),
    review_creation_date timestamp without time zone,
    review_answer_timestamp timestamp without time zone
);


ALTER TABLE public."order_reviews" OWNER TO postgres;

--
-- Name: PRODUCTS; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."products" (
    product_id character varying(32) NOT NULL,
    product_category_name character varying(46) NOT NULL,
    product_name_lenght smallint NOT NULL,
    product_description_lenght integer,
    product_photos_qty smallint,
    product_weight_g integer,
    product_lenght_cm smallint,
    product_height_cm smallint,
    product_width_cm smallint
);


ALTER TABLE public."products" OWNER TO postgres;

--
-- Name: SELLERS; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."sellers" (
    seller_id character varying(32) NOT NULL,
    seller_zip_code_prefix integer NOT NULL,
    seller_city character varying(40) NOT NULL,
    seller_state character varying(2) NOT NULL
);


ALTER TABLE public."sellers" OWNER TO postgres;

--
-- Name: CUSTOMER CUSTOMER_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."customers"
    ADD CONSTRAINT "customer_pkey" PRIMARY KEY (customer_id);


--
-- Name: ORDERS ORDERS_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."orders"
    ADD CONSTRAINT "orders_pkey" PRIMARY KEY (order_id);


--
-- Name: PRODUCTS PRODUCTS_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."products"
    ADD CONSTRAINT "products_pkey" PRIMARY KEY (product_id);


--
-- Name: SELLERS SELLERS_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."sellers"
    ADD CONSTRAINT "sellers_pkey" PRIMARY KEY (seller_id);


--
-- Name: ORDERS fk_customer; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."orders"
    ADD CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES public."customers"(customer_id);


--
-- Name: ORDER_ITEMS fk_order; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."order_items"
    ADD CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES public."orders"(order_id);


--
-- Name: ORDER_PAYMENTS fk_order; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."order_payments"
    ADD CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES public."orders"(order_id);


--
-- Name: ORDER_REVIEWS fk_order; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."order_reviews"
    ADD CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES public."orders"(order_id);


--
-- Name: ORDER_ITEMS fk_product; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."order_items"
    ADD CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES public."products"(product_id);


--

-- Name: ORDER_ITEMS fk_seller; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."order_items"
    ADD CONSTRAINT fk_seller FOREIGN KEY (seller_id) REFERENCES public."sellers"(seller_id);
