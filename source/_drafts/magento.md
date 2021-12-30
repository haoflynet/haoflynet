如果想对一个block禁用缓存，可以这样做

```xml
     <referenceBlock name="minicart" >
            <block class="Magento\Framework\View\Element\Text" cacheable="false" />
        </referenceBlock>
```