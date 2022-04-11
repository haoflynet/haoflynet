通配符证书限制

### Cloudflare 支持通配符 DNS 条目吗？

Cloudflare 支持所有客户计划中 DNS 管理的通配符'*'记录。企业客户可以使用通配符记录的完全代理。

#### 免费、专业 （PRO）和 商业（Business）版

Cloudflare 不代理通配符记录；只会作通配符子域直接传输，而没有任何 Cloudflare 性能、安全性或应用。因此，Wildcard 域在 Cloudflare DNS 应用中不会显示任何云（橙色或灰色）。如果要添加`*`CNAME 或 A 记录，先需要确保记录为灰色云才能创建记录。

要在通配符子域（例如：www）上获得 Cloudflare 保护，您需要在 Cloudflare DNS 设置中明确定义该记录。首先，登录您的 Cloudflare 账户并单击 DNS 应用。在此示例中，您将在 Cloudflare DNS 设置上添加“www”作为其自己的 CNAME 记录，并将云切换为橙色，以便启用 Cloudflare 的代理。

Cloudflare 企业版（Enterprise） 客户可以代理通配符记录。要了解有关企业版的更多信息，请[与我们联系](https://www.cloudflare.com/enterprise-service-request)。

通配符仅在最左侧的子域标签中有效。例如，无法添加 sub.*.example.com，但可以添加 *.sub.example.com。





指定nodejs版本需要将版本放到.nvmrc中，https://developers.cloudflare.com/pages/platform/build-configuration/

对pages主域名添加access policy，需要进入子域名编辑页面put一次域名





## Error 524: a timeout occurred

超时限制，免费账户100秒即超时



