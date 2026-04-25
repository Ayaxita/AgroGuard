erDiagram
    %% 账户与权限模块
    ACCOUNT_MYUSER {
        int id PK
        string username UK
        string password
        string realname
        string jobrole
        string staff_num
        int belong
        string mobile
    }

    AUTH_GROUP {
        int id PK
        string name UK
    }

    AUTH_PERMISSION {
        int id PK
        string name
        int content_type_id FK
        string codename
    }

    ACCOUNT_MYUSER_GROUP {
        int id PK
        int myuser_id FK
        int group_id FK
    }

    %% 基础信息模块 - 核心羊只表
    BASIC_BASICINFO {
        int id PK
        string ele_num UK
        string pre_num UK
        int variety
        int sex
        int purpose
        int manu_info_id FK
        string manu_info_name
        int state
        date birth
        date wea_date
        double weight
        int house_id FK
        int hurdle_id FK
        string house_name
        string hurdle_name
        int father_id FK
        int mother_id FK
        string f_ele_num
        string m_ele_num
        int belong
    }

    BASIC_BREEDERCONDITIONINFO {
        int id PK
        int basic_id FK
        date date
        int age
        double high
        double weight
    }

    BASIC_MANUINFO {
        int id PK
        string manu_name UK
        int scale
        int type
    }

    BASIC_CAPACITY {
        int id PK
        date start_date
        date end_date
        double mating_rate
        double lamb_num
        int belong
    }

    %% 繁殖模块
    E_BREED_BREEDINGINFO {
        int id PK
        date breeding_date
        date pre_production_date
        int breeding_way
        int ewe_id FK
        int ram_id FK
        int breeding_state
        int belong
    }

    E_BREED_LAMBINFO {
        int id PK
        int breeding_id FK
        int basic_id FK
        string logo UK
        string ele_num UK
        string pre_num UK
        int variety
        int sex
        int belong
    }

    E_BREED_PREGNANTINFO {
        int id PK
        int breeding_id FK
        date breeding_date
        date delivery_date
        int ram_id FK
        int ewe_id FK
        double Booroola
        int ewe_health
        int ewe_condition
        int lamb_ele_num
        int belong
    }

    E_BREED_POSTNATALINFO {
        int id PK
        int breeding_id FK
        date delivery_date
        int lamb_ele_num
        int belong
    }

    E_BREED_WEANINGINFO {
        int id PK
        int lamb_id FK
        date Delivery_date
        int feeding_way
        double Bir_weight
        double wea_weight
        int belong
    }

    E_BREED_ARTIFICIALFEEDINGINFO {
        int id PK
        int lamb_id FK
        date delivery_date
    }

    E_BREED_SEMENCOLLECTINFO {
        int id PK
        int basic_id FK
        date E_date
        double dilution_ratio
    }

    E_BREED_RUTINFO {
        int id PK
        int basic_id FK
        int age
        int breeding
    }

    %% 健康管理模块
    D_HEALTH_DISEASEINFO {
        int id PK
        int basic_id FK
        date disease_time
        string disease
        int belong
    }

    D_HEALTH_DEATHINFO {
        int id PK
        int basic_id FK
        date date
        int cause
        date t_time
        int belong
    }

    D_HEALTH_ABORTIONINFO {
        int id PK
        int basic_id FK
        date f_date
    }

    D_HEALTH_IMMUNIZATIONINFO {
        int id PK
        int basic_id FK
        date imm_date
        int vaccine_id FK
    }

    D_HEALTH_DRUGBATHINFO {
        int id PK
        int basic_id FK
        date take_time
    }

    D_HEALTH_NURSINGINFO {
        int id PK
        int basic_id FK
        date nur_time
    }

    D_HEALTH_QUARANTINEINFO {
        int id PK
        int basic_id FK
        date date
    }

    D_HEALTH_IMMUNIZATION_B_S {
        int id PK
        int basic_id FK
        string ele_num UK
    }

    %% 群体管理模块
    COLONY_HOUSEINFO {
        int id PK
        string name
        int pid
        date build_time
        int function
        double area
        int sheep_quantity
        int belong
    }

    COLONY_TRANSFERINFO {
        int id PK
        int basic_id FK
        int new_house_id FK
        int old_house_id FK
        date trans_time
        int belong
    }

    COLONY_DISINFECTIONINFO {
        int id PK
        int house_id FK
        date date
        string drug
        int belong
    }

    COLONY_MAINTENANCEINFO {
        int id PK
        int house_id FK
        date M_time
        double M_cost
    }

    %% 仓库管理模块
    H_STORE_FEEDINGIN {
        int id PK
        int type
        string f_name
        int ingredientsType
        date buy_time
        double quantity
        double unit_price
        double total_price
        int belong
    }

    H_STORE_FEEDING_OUT {
        int id PK
        string outbound_no UK
        int type
        date delivery_time
        int num
        int belong
    }

    H_STORE_VACCINE_IN {
        int id PK
        string v_name
        int type
        date produce_date
        date expiration_date
        int in_amount
        double unit_price
        int belong
    }

    H_STORE_VACCINE_OUT {
        int id PK
        string outbound_no UK
        string v_name
        int type
        date delivery_time
        int num
        int belong
    }

    H_STORE_INVENTORY {
        int id PK
        int type
        string goods
        int ingredientsType
        double quantity
        double stockPrice
        int belong
    }

    %% 销售与屠宰模块
    G_SLAUGHTER_S_SALESINFO {
        int id PK
        string ele_num UK
        int basic_id FK
        date sales_date
        double unit_price
        double weight
        double total_price
        int belong
    }

    G_SLAUGHTER_G_SALESINFO {
        int id PK
        date sales_date
        string sales_order
        int type
        double unit_price
        double weight
        double total_price
        int belong
    }

    G_SLAUGHTER_BINFORMATIONINFO {
        int id PK
        int basic_id FK
        date date
        double back_fat_thickness
        double net_meat_ratio
    }

    G_SLAUGHTER_SLAUGHTERSEGMENTINFO {
        int id PK
        string basic_id
        date date
        double net_meat_weight
    }

    G_SLAUGHTER_ECONOMICINFO {
        int id PK
        string basic_id
        double in_weight
        double out_weight
        double intake
        double cost
    }

    %% 统计分析模块
    ANALYSIS_DAILY_INCOME {
        int id PK
        date f_date
        double number_0
        double value_0
        double dung_value
        double wool_value
        double feed_value
        int belong
    }

    ANALYSIS_DAILY_SHEET {
        int id PK
        date f_date
        double buysheep_fees
        double caoliao_fees
        double food_fees
        double labor_fees
        double total_fees
        int belong
    }

    ANALYSIS_DAILY_STOCK_SHEET {
        int id PK
        date date
        double garlicskin_num
        double garlicskin_val
        double corn_num
        double corn_val
    }

    SHEEP_ASSETINFO {
        int id PK
        int variety
        int number
        double sum_value
        date f_date
        int belong
    }

    SHEEP_ASSET_STANDARDINFO {
        int id PK
        int variety
        double unit_price
        date f_date
    }

    %% 供应与供应商
    SUPPLY_F_SUPPLIERSINFO {
        int id PK
        string supplier_name UK
        string sup_linkman
        string sup_contact
        string mail
        int belong
    }

    SUPPLY_V_SUPPLIERSINFO {
        int id PK
        string supplier_name
        string sale_type
        string sup_linkman
        int belong
    }

    SUPPLY_COMMODITYINFO {
        int id PK
        int type
        string cname
        int belong
    }

    %% 网站内容管理
    NEWS {
        int id PK
        int category
        string title
        text content
        string author
        datetime pubdate
    }

    CMS_ADM {
        int id PK
        string name
        string password
        string email
        datetime create_time
    }

    CMS_CATEGORY {
        int id PK
        int parent_id
        string name
        int level
    }

    CMS_ARTICLE {
        int id PK
        int category_id FK
        string title
        string author
        text content
        datetime create_time
    }

    %% ==================== 关系定义 ====================

    ACCOUNT_MYUSER_GROUP }o--|| ACCOUNT_MYUSER : "myuser_id"
    ACCOUNT_MYUSER_GROUP }o--|| AUTH_GROUP : "group_id"
    AUTH_GROUP ||--o{ ACCOUNT_MYUSER_GROUP : "users"

    BASIC_BASICINFO }o--|| BASIC_MANUINFO : "manu_info_id"
    BASIC_BASICINFO }o--|| COLONY_HOUSEINFO : "house_id"
    BASIC_BASICINFO }o|| BASIC_BASICINFO : "father_id"
    BASIC_BASICINFO }o|| BASIC_BASICINFO : "mother_id"
    BASIC_BREEDERCONDITIONINFO }o--|| BASIC_BASICINFO : "basic_id"

    E_BREED_LAMBINFO }o--|| E_BREED_BREEDINGINFO : "breeding_id"
    E_BREED_LAMBINFO }o--|| BASIC_BASICINFO : "basic_id"

    E_BREED_PREGNANTINFO }o--|| E_BREED_BREEDINGINFO : "breeding_id"
    E_BREED_POSTNATALINFO }o--|| E_BREED_BREEDINGINFO : "breeding_id"

    E_BREED_WEANINGINFO }o--|| E_BREED_LAMBINFO : "lamb_id"
    E_BREED_ARTIFICIALFEEDINGINFO }o--|| E_BREED_LAMBINFO : "lamb_id"
    E_BREED_SEMENCOLLECTINFO }o--|| BASIC_BASICINFO : "basic_id"
    E_BREED_RUTINFO }o--|| BASIC_BASICINFO : "basic_id"

    D_HEALTH_DISEASEINFO }o--|| BASIC_BASICINFO : "basic_id"
    D_HEALTH_DEATHINFO }o--|| BASIC_BASICINFO : "basic_id"
    D_HEALTH_ABORTIONINFO }o--|| BASIC_BASICINFO : "basic_id"
    D_HEALTH_IMMUNIZATIONINFO }o--|| BASIC_BASICINFO : "basic_id"
    D_HEALTH_DRUGBATHINFO }o--|| BASIC_BASICINFO : "basic_id"
    D_HEALTH_NURSINGINFO }o--|| BASIC_BASICINFO : "basic_id"
    D_HEALTH_QUARANTINEINFO }o--|| BASIC_BASICINFO : "basic_id"
    D_HEALTH_IMMUNIZATION_B_S }o--|| BASIC_BASICINFO : "basic_id"

    COLONY_TRANSFERINFO }o--|| BASIC_BASICINFO : "basic_id"
    COLONY_TRANSFERINFO }o--|| COLONY_HOUSEINFO : "new_house_id"
    COLONY_TRANSFERINFO }o--|| COLONY_HOUSEINFO : "old_house_id"
    COLONY_DISINFECTIONINFO }o--|| COLONY_HOUSEINFO : "house_id"
    COLONY_MAINTENANCEINFO }o--|| COLONY_HOUSEINFO : "house_id"

    G_SLAUGHTER_S_SALESINFO }o--|| BASIC_BASICINFO : "basic_id"
    G_SLAUGHTER_BINFORMATIONINFO }o--|| BASIC_BASICINFO : "basic_id"

    CMS_ARTICLE }o--|| CMS_CATEGORY : "category_id"