-- auto-generated definition
create table wechatpay_gonghj
(
    id            int auto_increment
        primary key,
    name          varchar(10)                         null comment '姓名',
    app           varchar(10)                         null comment '支付宝、微信、其他应用',
    time          varchar(20)                         null comment '交易创建时间',
    origin        varchar(100)                        null comment '交易来源地(微信无)',
    counter_party varchar(100)                        null comment '交易对方',
    commodity     varchar(150)                        null comment '商品名称',
    amount        varchar(20)                         null comment '金额（元）',
    in_exp        varchar(20)                         null comment '收/支',
    is_cal        int(2)    default 1                 null comment '资金状态',
    create_time   timestamp default CURRENT_TIMESTAMP null comment '数据创建时间',
    update_time   timestamp default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP comment '数据最后更新时间'
);

create index index_time
    on wechatpay_gonghj (time);



-- auto-generated definition
create table alipay_gonghj
(
    id            int auto_increment
        primary key,
    name          varchar(10)                         null comment '姓名',
    app           varchar(10)                         null comment '支付宝、微信、其他应用',
    time          varchar(20)            null comment '交易创建时间',
    origin        varchar(100)           null comment '交易来源地',
    counter_party varchar(100)           null comment '交易对方',
    commodity     varchar(150)           null comment '商品名称',
    amount        varchar(20)            null comment '金额（元）',
    in_exp        varchar(20)            null comment '收/支',
    is_cal        varchar(2) default '1' null comment '资金状态'
    create_time   timestamp default CURRENT_TIMESTAMP null comment '数据创建时间',
    update_time   timestamp default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP comment '数据最后更新时间'
);

create index index_created_time
    on alipay_gonghj (created_time);



-- auto-generated definition
create table wechatpay_origin_zhuangyc
(
    created_time          varchar(20)  null comment '交易时间',
    type                  varchar(32)  null comment '交易类型',
    counter_party         varchar(100) null comment '交易对方',
    commodity             varchar(150) null comment '商品',
    in_exp                varchar(20)  null comment '收/支',
    amount                varchar(20)  null comment '金额(元)',
    method                varchar(50)  null comment '支付方式',
    status                varchar(20)  null comment '当前状态',
    transaction_number    varchar(100) not null comment '交易单号'
        primary key,
    merchant_order_number varchar(100) null comment '商户单号',
    remark                varchar(255) null comment '备注'
);

create index index_created_time
    on wechatpay_origin_zhuangyc (created_time);




-- auto-generated definition
create table alipay_origin_zhuangyc
(
    transaction_number    varchar(100) not null comment '交易号'
        primary key,
    merchant_order_number varchar(100) null comment '商家订单号',
    created_time          varchar(20)  null comment '交易创建时间',
    pay_time              varchar(20)  null comment '付款时间',
    updated_time          varchar(20)  null comment '最近修改时间',
    origin                varchar(100) null comment '交易来源地',
    type                  varchar(32)  null comment '类型',
    counter_party         varchar(100) null comment '交易对方',
    commodity             varchar(150) null comment '商品名称',
    amount                varchar(20)  null comment '金额（元）',
    in_exp                varchar(20)  null comment '收/支',
    status                varchar(20)  null comment '交易状态',
    service_charge        varchar(20)  null comment '服务费（元）',
    refund                varchar(20)  null comment '成功退款',
    remark                varchar(255) null comment '备注',
    fund_status           varchar(20)  null comment '资金状态',
    crsj				  timestamp default CURRENT_TIMESTAMP null comment '数据插入时间',
    gxsj				  timestamp default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP comment '数据插入时间'
);

create index index_created_time
    on alipay_origin_zhuangyc (created_time);



