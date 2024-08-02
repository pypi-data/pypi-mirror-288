AlmaSQL

<details>
<summary>Directives</summary>

Directives are functions that can extend AlmaSQL by customizing the way an expression renders.

Using a directive in your template is as simple as calling a function in a template expression.

AlmaSQL includes a number of built-in directives like `set` and `values`.

Users can also write their own custom directives.

<details>
<summary>set</summary>

Imagine table `book` and columns `id`, `title`, and `is_active`.
And you want to update book by id.

```jinja
UPDATE book
SET title = :title, is_active = :is_active
WHERE id = :id
```

But when you need to modify column, you need to change the query template.
What if you forgot to do it? This will lead to unexpected bugs.
So better to use directives that, depending on the arguments,
will render the required columns and values.

```jinja
UPDATE book{{ set({'title': 'Why do I love almasql?', 'is_active': True}) }}
WHERE id = :id
```
</details>
</details>
