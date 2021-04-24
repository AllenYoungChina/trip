# 慕旅游网接口文档
RESTful风格接口
* 200 请求数据成功
* 201 提交数据成功
* 400 请求参数错误
* 401 未登录
* 403 没有权限
* 500 服务器正忙

## 接口请求地址
1. 测试环境
http://test.xxx.com/
2. 生产环境
http://xxx.com/
   
## 错误代码及文字提示
```json
{
  "error_code": "400000",
  "error_msg": "该字段不能为空。",
  "error_list": {
    "password": [
      "该字段不能为空。"
    ]
  }
}
```

## 请求头添加内容

## 分页
### 分页请求参数
| 字段 | 类型 | 说明 |
| --- | --- | --- |
| page | int | 当前页（默认为第一页） |

### 分页响应参数
| 字段 | 类型 | 说明 |
| --- | --- | --- |
| meta |    | 分页元数据，解释如下 |
| total_count | int | 根据传入条件检索到的记录总数 |
| current_page | int | 当前页面 |
| page_count | int | 总页数 |
| objects | array | objects为返回的对象列表 |

## 接口列表
### 1. 系统模块
* [1.1 轮播图接口](./system/slider_list.md)

### 2. 景点模块
* [2.1 景点列表接口](./sight/sight_list.md)
