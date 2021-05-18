google 服务

## Map地图服务

- vue推荐使用[vue-google-autocomplete](https://github.com/olefirenko/vue-google-autocomplete)做地址的自动完成，只需要按照其`README`开通对应的API，然后在`Credentials`拿到`API KEY`即可，它主要是用的是`AutocompletionService`，该组件支持这样几个自定义搜索参数:
  - types: 默认值为`address`还支持`geocode/establishment/address/(regions)/(cities)`
  - country: 限制搜索国家
  - getAddressData会返回addressData(administrative_area_level_1, country, latitude, locality, longitude), placeResultData(address_components(包含行政区层级), place_id), id(这只是map组件的id)
  - 可以通过inputChange事件和update方法来修改自动填充的内容

## GTM(Google Tag Manager)

- 有了它就不用每次添加一个新的服务(tag)都去修改代码了，因此服务添加多了也不会影响网站的首次加载速度
- 在新建了账号后，就可以选择`Tags->New`，例如可以添加`Google Analytics 4`

