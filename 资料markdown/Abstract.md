# Abstract

Grassland crop management has long relied on paper records and manual statistics, which leads to scattered data and slow updates. Pest and disease control information is often delayed. To address this, an intelligent monitoring system for grassland crop pests and diseases (hereinafter referred to as the grassland pest and disease monitoring system) was designed and implemented, bringing basic archives, field records, pest control, supply chain and sales settlement into a unified online platform.

The back end uses Python Flask with blueprints to split business modules such as authentication, archives, fields, pest control, supplies and sales. SQLAlchemy handles MySQL operations, JWT manages login authentication, and APScheduler runs a daily scheduled task to refresh pest and disease warnings automatically. The front end is built with Vue 3 and Element Plus, using Vue Router and Pinia for routing and state management, and ECharts for chart rendering. The system also integrates the Zhipu GLM API to provide an agricultural Q&A assistant that can query the database via Function Calling. The project is deployed with Docker Compose orchestrating MySQL, Flask and Nginx services.

The system covers grassland archive maintenance, field management, breeding tracking, pest control with automatic warnings, supply storage, harvesting and sales, asset valuation and daily income statistics. It supports Excel batch imports and QR code tracing, with two-level permissions for administrators and regular users. In practice, the system moved fragmented manual workflows online, shortening data query time and pest response delays while reducing repetitive entry and statistics work.

**Key words:** Grassland crop management; pest and disease warning; Flask; Vue.js; MySQL
