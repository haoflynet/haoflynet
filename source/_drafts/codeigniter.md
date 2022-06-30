

## 数据库操作

### 增删改查

```php
$db->getLastQuery()->getQuery;	// 获取上一次查询的SQL语句

# 查询操作
$user = $userModel->from('table')->find($id);	// 通过id查询单条记录
$user = $userModel->from('table')->get()->row();	// 获取一条记录

$this->db
  ->where('name', $name)	// where查询
  ->where('name !=', $name)
  ->where('id < ', 10)
  ->like('name', 'hao')	// like查询
  ->or_like('name', 'fly')	// or like查询
  ->limit(10, 20)	// limit 20, 10操作，注意两个数字是反的
  ->group_by('id')	// group by操作
  ->join('posts', 'posts.user_id = users.id AND ...多个条件也可以', 'LEFT')	// left join 操作
  ->select(*)	// 不加这一句默认也是select *
  ->select('*, group_concat(`posts`.`id`) as post_ids')	// group_concat操作
  ->order_by('id', 'DESC');	// order by 操作

# ... and (... or ...)，需要借助group
$this->db->where('field', $value)
$this->db->group_start()
  ->or_group_start()
  ->like('first_name', $keyword)
  ->or_like('...')
  ->or_where
  ->group_end()
  
# COUNT
$this->db->count_all_results('表名', false);	// count操作，如果前面有->from(表名)，这里第一个参数可以留空字符串，如果count后还要做其他的查询操作，第二个参数可以设置为false

# 创建操作
$user = new \App\Entities\User();
$user->fill($data);
$userModel->save($user);

$this->db->insert('table', $data);

# 更新操作
$user->username = 'haofly';
$userModel->save($user);

# 删除操作
$this->db->delete('table', ['id' => 123]);	// 根据条件删除数据
```

### migrations

- 好像是数据库里面`migrations`表里面的`version`设置为哪个文件的前缀就会执行那个文件



session写入失败

```php
A PHP Error was encountered

Severity: Warning

Message: mkdir(): Invalid path
```

可能之前设置的是window或者其他没有权限的路径，可以这样配置$config['sess_save_path'] = sys_get_temp_dir();





https://gist.github.com/yidas/30a611449992b0fac173267951e5f17f
