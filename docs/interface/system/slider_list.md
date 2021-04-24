## 首页轮播图接口

### 请求地址
/system/slider/list/

### 请求方式
GET

### 请求参数
| 字段 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| types | true | int | 轮播图类型（10：首页轮播图） |

### 响应结果
```json
{
  "meta": {
    "total_count": 2,
    "page_count": 1,
    "current_page": 1
  },
  "objects": [
    {
      "pk": 1,
      "name": "轮播图1",
      "desc": null,
      "img": "http://xxx.com/media/slider/banner/banner1.jpg",
      "target_url": null
    },
    {
      "pk": 2,
      "name": "轮播图2",
      "desc": null,
      "img": "http://xxx.com/media/slider/banner/banner2.jpg",
      "target_url": null
    }
  ]
}
```
### 响应字段说明
| 字段 | 类型 | 说明 |
| --- | --- | --- |
| meta |    | 分页元数据 |
| objects |    | objects下为轮播图对象，详细如下 |
| pk | int | 记录ID |
| name | string | 名称 |
| desc | string | 描述信息 |
| img | string | 图片地址 |
| target_url | string | 跳转地址 |
