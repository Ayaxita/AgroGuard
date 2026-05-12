# 附录A  草地病虫害监测系统核心代码

草地病虫害监测系统包括用户登录认证、草地档案与田间管理、批次管理、草地护理与预警、库存管理与产品销售、草地病虫害监测分析以及大模型问答助手等模块，该部分仅展示核心代码。

## 1.用户登录认证核心代码







图A.1  用户登录后端接口代码（文件：meadow-be/App/login_auth/views.py，第25行~第66行）







图A.2  JWT全局拦截器代码（文件：meadow-be/app.py，第11行~第40行）

## 2.草地档案核心代码







图A.3  档案多条件查询分页代码（文件：meadow-be/App/basic/views.py，第133行~第232行）







图A.4  档案新增接口代码（文件：meadow-be/App/basic/views.py，第439行~第518行）







图A.5  田间长势记录查询代码（文件：meadow-be/App/basic/views.py，第1444行~第1523行）

## 3.批次管理核心代码







图A.6  生长周期记录查询代码（文件：meadow-be/App/propagation/views.py，第97行~第196行）







图A.7  阶段切换信息查询代码（文件：meadow-be/App/propagation/views.py，第400行~第500行）

## 4.草地护理核心代码







图A.8  草地防护记录关联查询代码（文件：meadow-be/App/pest_control/views.py，第97行~第196行）







图A.9  新增草地防护记录代码（文件：meadow-be/App/pest_control/views.py，第721行~第782行）

## 5.预警信息核心代码







图A.10  APScheduler定时任务初始化代码（文件：meadow-be/App/task.py，第203行~第223行）







图A.11  预警信息定时更新SQL代码（文件：meadow-be/App/task.py，第8行~第193行）

## 6.库存管理核心代码







图A.12  库存预警校验代码（文件：meadow-be/App/h_store/views.py，第77行~第120行）







图A.13  防护物资出库新增代码（文件：meadow-be/App/h_store/views.py，第656行~第720行）

## 7.产品销售核心代码







图A.14  销售后资产扣减代码（文件：meadow-be/App/analysis/views.py，第518行~第597行）

## 8.草地病虫害监测分析核心代码







图A.15  资产估值批量计算代码（文件：meadow-be/App/analysis/views.py，第192行~第265行）







图A.16  日收益报表查询代码（文件：meadow-be/App/analysis/views.py，第857行~第950行）

## 9.大模型问答助手核心代码







图A.17  对话接口核心代码（文件：meadow-be/App/chatbox/views.py，第42行~第125行）







图A.18  工具执行函数代码（文件：meadow-be/App/chatbox/views.py，第23行~第39行）







图A.19  数据库查询工具代码（文件：meadow-be/App/chatbox/db_tools.py，第50行~第80行）
