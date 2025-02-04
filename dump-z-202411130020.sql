PGDMP                   
    |            z    17.0    17.0 E               0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            	           1262    16714    z    DATABASE     u   CREATE DATABASE z WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE z;
                     postgres    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
                     pg_database_owner    false            
           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                        pg_database_owner    false    4            �            1259    16716    address    TABLE     �   CREATE TABLE public.address (
    id integer NOT NULL,
    index integer,
    region character varying,
    city character varying,
    street character varying,
    number integer
);
    DROP TABLE public.address;
       public         heap r       postgres    false    4            �            1259    16715    address_id_seq    SEQUENCE     �   CREATE SEQUENCE public.address_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.address_id_seq;
       public               postgres    false    4    218                       0    0    address_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.address_id_seq OWNED BY public.address.id;
          public               postgres    false    217            �            1259    16776    material    TABLE     x   CREATE TABLE public.material (
    id integer NOT NULL,
    name character varying,
    defect_rate double precision
);
    DROP TABLE public.material;
       public         heap r       postgres    false    4            �            1259    16775    material_id_seq    SEQUENCE     �   CREATE SEQUENCE public.material_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.material_id_seq;
       public               postgres    false    228    4                       0    0    material_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.material_id_seq OWNED BY public.material.id;
          public               postgres    false    227            �            1259    16785    material_product    TABLE     s   CREATE TABLE public.material_product (
    id integer NOT NULL,
    id_product integer,
    id_material integer
);
 $   DROP TABLE public.material_product;
       public         heap r       postgres    false    4            �            1259    16784    material_product_id_seq    SEQUENCE     �   CREATE SEQUENCE public.material_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.material_product_id_seq;
       public               postgres    false    230    4                       0    0    material_product_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.material_product_id_seq OWNED BY public.material_product.id;
          public               postgres    false    229            �            1259    16802    partner_product    TABLE     �   CREATE TABLE public.partner_product (
    id integer NOT NULL,
    id_product integer,
    id_partner integer,
    quantity integer,
    date_of_sale date
);
 #   DROP TABLE public.partner_product;
       public         heap r       postgres    false    4            �            1259    16801    partner_product_id_seq    SEQUENCE     �   CREATE SEQUENCE public.partner_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.partner_product_id_seq;
       public               postgres    false    232    4                       0    0    partner_product_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.partner_product_id_seq OWNED BY public.partner_product.id;
          public               postgres    false    231            �            1259    16734    partners    TABLE     3  CREATE TABLE public.partners (
    id_partner integer NOT NULL,
    type_partner_id integer,
    company_name character varying,
    ur_adress integer,
    inn bigint,
    director_name character varying,
    phone character varying,
    email character varying,
    rating integer,
    discount integer
);
    DROP TABLE public.partners;
       public         heap r       postgres    false    4            �            1259    16733    partners_id_partner_seq    SEQUENCE     �   CREATE SEQUENCE public.partners_id_partner_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.partners_id_partner_seq;
       public               postgres    false    222    4                       0    0    partners_id_partner_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.partners_id_partner_seq OWNED BY public.partners.id_partner;
          public               postgres    false    221            �            1259    16762    product    TABLE     �   CREATE TABLE public.product (
    id integer NOT NULL,
    type integer,
    description character varying,
    art integer,
    price double precision,
    size double precision,
    class integer
);
    DROP TABLE public.product;
       public         heap r       postgres    false    4            �            1259    16761    product_id_seq    SEQUENCE     �   CREATE SEQUENCE public.product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.product_id_seq;
       public               postgres    false    4    226                       0    0    product_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.product_id_seq OWNED BY public.product.id;
          public               postgres    false    225            �            1259    16753    product_type    TABLE     |   CREATE TABLE public.product_type (
    id integer NOT NULL,
    name character varying,
    coefficient double precision
);
     DROP TABLE public.product_type;
       public         heap r       postgres    false    4            �            1259    16752    product_type_id_seq    SEQUENCE     �   CREATE SEQUENCE public.product_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.product_type_id_seq;
       public               postgres    false    224    4                       0    0    product_type_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.product_type_id_seq OWNED BY public.product_type.id;
          public               postgres    false    223            �            1259    16725    type_company    TABLE     Z   CREATE TABLE public.type_company (
    id integer NOT NULL,
    name character varying
);
     DROP TABLE public.type_company;
       public         heap r       postgres    false    4            �            1259    16724    type_company_id_seq    SEQUENCE     �   CREATE SEQUENCE public.type_company_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.type_company_id_seq;
       public               postgres    false    4    220                       0    0    type_company_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.type_company_id_seq OWNED BY public.type_company.id;
          public               postgres    false    219            D           2604    16719 
   address id    DEFAULT     h   ALTER TABLE ONLY public.address ALTER COLUMN id SET DEFAULT nextval('public.address_id_seq'::regclass);
 9   ALTER TABLE public.address ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    218    217    218            I           2604    16779    material id    DEFAULT     j   ALTER TABLE ONLY public.material ALTER COLUMN id SET DEFAULT nextval('public.material_id_seq'::regclass);
 :   ALTER TABLE public.material ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    228    227    228            J           2604    16788    material_product id    DEFAULT     z   ALTER TABLE ONLY public.material_product ALTER COLUMN id SET DEFAULT nextval('public.material_product_id_seq'::regclass);
 B   ALTER TABLE public.material_product ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    230    229    230            K           2604    16805    partner_product id    DEFAULT     x   ALTER TABLE ONLY public.partner_product ALTER COLUMN id SET DEFAULT nextval('public.partner_product_id_seq'::regclass);
 A   ALTER TABLE public.partner_product ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    232    231    232            F           2604    16737    partners id_partner    DEFAULT     z   ALTER TABLE ONLY public.partners ALTER COLUMN id_partner SET DEFAULT nextval('public.partners_id_partner_seq'::regclass);
 B   ALTER TABLE public.partners ALTER COLUMN id_partner DROP DEFAULT;
       public               postgres    false    222    221    222            H           2604    16765 
   product id    DEFAULT     h   ALTER TABLE ONLY public.product ALTER COLUMN id SET DEFAULT nextval('public.product_id_seq'::regclass);
 9   ALTER TABLE public.product ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    225    226    226            G           2604    16756    product_type id    DEFAULT     r   ALTER TABLE ONLY public.product_type ALTER COLUMN id SET DEFAULT nextval('public.product_type_id_seq'::regclass);
 >   ALTER TABLE public.product_type ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    224    223    224            E           2604    16728    type_company id    DEFAULT     r   ALTER TABLE ONLY public.type_company ALTER COLUMN id SET DEFAULT nextval('public.type_company_id_seq'::regclass);
 >   ALTER TABLE public.type_company ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    220    219    220            �          0    16716    address 
   TABLE DATA           J   COPY public.address (id, index, region, city, street, number) FROM stdin;
    public               postgres    false    218   �O       �          0    16776    material 
   TABLE DATA           9   COPY public.material (id, name, defect_rate) FROM stdin;
    public               postgres    false    228   Q                 0    16785    material_product 
   TABLE DATA           G   COPY public.material_product (id, id_product, id_material) FROM stdin;
    public               postgres    false    230   }Q                 0    16802    partner_product 
   TABLE DATA           ]   COPY public.partner_product (id, id_product, id_partner, quantity, date_of_sale) FROM stdin;
    public               postgres    false    232   �Q       �          0    16734    partners 
   TABLE DATA           �   COPY public.partners (id_partner, type_partner_id, company_name, ur_adress, inn, director_name, phone, email, rating, discount) FROM stdin;
    public               postgres    false    222   hR       �          0    16762    product 
   TABLE DATA           Q   COPY public.product (id, type, description, art, price, size, class) FROM stdin;
    public               postgres    false    226   }T       �          0    16753    product_type 
   TABLE DATA           =   COPY public.product_type (id, name, coefficient) FROM stdin;
    public               postgres    false    224   �U       �          0    16725    type_company 
   TABLE DATA           0   COPY public.type_company (id, name) FROM stdin;
    public               postgres    false    220   %V                  0    0    address_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.address_id_seq', 7, true);
          public               postgres    false    217                       0    0    material_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.material_id_seq', 5, true);
          public               postgres    false    227                       0    0    material_product_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.material_product_id_seq', 5, true);
          public               postgres    false    229                       0    0    partner_product_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.partner_product_id_seq', 16, true);
          public               postgres    false    231                       0    0    partners_id_partner_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.partners_id_partner_seq', 7, true);
          public               postgres    false    221                       0    0    product_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.product_id_seq', 5, true);
          public               postgres    false    225                       0    0    product_type_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.product_type_id_seq', 4, true);
          public               postgres    false    223                       0    0    type_company_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.type_company_id_seq', 4, true);
          public               postgres    false    219            M           2606    16723    address address_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.address
    ADD CONSTRAINT address_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.address DROP CONSTRAINT address_pkey;
       public                 postgres    false    218            W           2606    16783    material material_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.material
    ADD CONSTRAINT material_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.material DROP CONSTRAINT material_pkey;
       public                 postgres    false    228            Y           2606    16790 &   material_product material_product_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.material_product
    ADD CONSTRAINT material_product_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.material_product DROP CONSTRAINT material_product_pkey;
       public                 postgres    false    230            [           2606    16807 $   partner_product partner_product_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.partner_product
    ADD CONSTRAINT partner_product_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.partner_product DROP CONSTRAINT partner_product_pkey;
       public                 postgres    false    232            Q           2606    16741    partners partners_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.partners
    ADD CONSTRAINT partners_pkey PRIMARY KEY (id_partner);
 @   ALTER TABLE ONLY public.partners DROP CONSTRAINT partners_pkey;
       public                 postgres    false    222            U           2606    16769    product product_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.product DROP CONSTRAINT product_pkey;
       public                 postgres    false    226            S           2606    16760    product_type product_type_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.product_type
    ADD CONSTRAINT product_type_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.product_type DROP CONSTRAINT product_type_pkey;
       public                 postgres    false    224            O           2606    16732    type_company type_company_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.type_company
    ADD CONSTRAINT type_company_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.type_company DROP CONSTRAINT type_company_pkey;
       public                 postgres    false    220            _           2606    16796 2   material_product material_product_id_material_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.material_product
    ADD CONSTRAINT material_product_id_material_fkey FOREIGN KEY (id_material) REFERENCES public.material(id);
 \   ALTER TABLE ONLY public.material_product DROP CONSTRAINT material_product_id_material_fkey;
       public               postgres    false    228    230    4695            `           2606    16791 1   material_product material_product_id_product_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.material_product
    ADD CONSTRAINT material_product_id_product_fkey FOREIGN KEY (id_product) REFERENCES public.product(id);
 [   ALTER TABLE ONLY public.material_product DROP CONSTRAINT material_product_id_product_fkey;
       public               postgres    false    230    4693    226            a           2606    16813 /   partner_product partner_product_id_partner_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.partner_product
    ADD CONSTRAINT partner_product_id_partner_fkey FOREIGN KEY (id_partner) REFERENCES public.partners(id_partner);
 Y   ALTER TABLE ONLY public.partner_product DROP CONSTRAINT partner_product_id_partner_fkey;
       public               postgres    false    232    222    4689            b           2606    16808 /   partner_product partner_product_id_product_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.partner_product
    ADD CONSTRAINT partner_product_id_product_fkey FOREIGN KEY (id_product) REFERENCES public.product(id);
 Y   ALTER TABLE ONLY public.partner_product DROP CONSTRAINT partner_product_id_product_fkey;
       public               postgres    false    232    4693    226            \           2606    16742 &   partners partners_type_partner_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.partners
    ADD CONSTRAINT partners_type_partner_id_fkey FOREIGN KEY (type_partner_id) REFERENCES public.type_company(id);
 P   ALTER TABLE ONLY public.partners DROP CONSTRAINT partners_type_partner_id_fkey;
       public               postgres    false    220    4687    222            ]           2606    16747     partners partners_ur_adress_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.partners
    ADD CONSTRAINT partners_ur_adress_fkey FOREIGN KEY (ur_adress) REFERENCES public.address(id);
 J   ALTER TABLE ONLY public.partners DROP CONSTRAINT partners_ur_adress_fkey;
       public               postgres    false    4685    218    222            ^           2606    16770    product product_type_fkey    FK CONSTRAINT     |   ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_type_fkey FOREIGN KEY (type) REFERENCES public.product_type(id);
 C   ALTER TABLE ONLY public.product DROP CONSTRAINT product_type_fkey;
       public               postgres    false    4691    226    224            �   %  x���]N�@��ﬢ+h懡��Ƈ6�����3B�@����yf�&��w�[�5����OR�ȍ�|� �>>y�����?����a��Md��d��kp��;�Z�Ͳޡ7��#n_�����uD�����(J�S8�]̀1�q6� �C_#�J��
f4�j�Fed2W���WO�,�oP<��&�h@����t����Jocr�g� J�-�~��1'D��O#�V�8]��UY`]��Q�Ssh�s�H��cJ�����ˌ]������"9u�TJ}�@jb      �   i   x�}ʻ	�@��x�
+ϻ��b|��F�6�)�Z��ȭ�d�>GX�Á[G*r�%a��E-�	3��ڞH��/+����p!j��@B4�`D�凈�ə� �A�         &   x�3�4�4�2�B.cNc i�i$M9M9��b���� K�-         �   x�U���0D�����{I�uɱ�:=v�X�d������9�����0�����W����A����h����1�rh
�G��꿢�̋�(��ԩČ�E-oC�c(����ܪ(�{�V���-����\������z����w�����[�M��ϋ���K;�      �     x�U�Qn�@���S�Ȼ���'�	�m�0��"���M+U�C�4=�ۄցB�0{���`,!�����f4)�[��[���/#���O�eV��1�{��gd.��-~��i����,U:��4�j2)�Ӳ�W����wzd����ԡ]� ��{�y��O��㽿F>�B@��P�Q161�.ݸ9r�a�U9"�!�P�_���x���1q��ؠ�;ķR֯��o��� �.6!���AZi��D�1���UQ�g�I#M�@6��@���ǒB����� nfS�}p����눿H��A���:��m�vRǘ`E)*�ܼ�Ʈ[���eQ��(p�`�ʌ����A�d����0���rtz����-�\il�,
���čK� /"�b��$R�l�{��$,�)OiK�`���:8����(=�>�����,�I9ԉ9����O�����|��
@KkU��F�2vЅ�"���[��	�[̓W37~=u�Jzoy�
\t;��3؈�*      �     x�u�MN�0���)z��$��s�2H�`$6,�X�a?4����
΍xn�AU"�~~_mC��������nyB����z�T��A���������	�7��"_z)Ő\
�}�ԙ��͕�䈟�x/��3��zÇ�_Q�A���c���������rH�ku�
�	��#���t� c���|��F1��&K&欝'甗]�u��nmEc�\ʭ��Y�e`�kd���S1Y���e"��T��*�:�5~�ąBkl�������h��f"��      �   u   x�e���0�wUP�I�v7|�H �a	��ia�#V��:������|Q|��b�^�2M>�o���aG#8Q$[�/#I��.%�I%*o��_�Ï�����,�`�zo�Q�      �   (   x�3�0��8/�A.c���"& #F��� ���     