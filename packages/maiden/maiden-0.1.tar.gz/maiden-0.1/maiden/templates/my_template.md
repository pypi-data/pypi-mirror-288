# <% FROM source1.yaml GET 'integration.header' %>

- By: <% FROM source1.yaml GET 'integration.author' %>
- Date: <% FROM source1.yaml GET 'integration.date' %>

Content:
<% FROM source1.yaml GET 'integration.content' %>
