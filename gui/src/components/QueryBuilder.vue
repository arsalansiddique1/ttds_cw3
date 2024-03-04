<template>
    <div class="vue-root">
      <div class="demo-description">
        
      </div>
      <smart-query-builder id="queryBuilder"></smart-query-builder>
    </div>
  </template>
  
  <script>
  import { onMounted } from "vue";
  import "smart-webcomponents/source/styles/smart.default.css";
  import "smart-webcomponents/source/modules/smart.querybuilder.js";
  
  export default {
    name: "app",
    setup() {
      onMounted(() => {
        window.Smart(
          "#queryBuilder",
          class {
            get properties() {
              return {
                allowDrag: true,
                fields: [
                  {
                    label: "Id",
                    dataField: "id",
                    dataType: "number"
                  },
                  {
                    label: "Product",
                    dataField: "productName",
                    dataType: "string"
                  },
                  {
                    label: "Unit Price",
                    dataField: "price",
                    dataType: "number"
                  },
                  {
                    label: "Purchased",
                    dataField: "purchased",
                    dataType: "datetime"
                  },
                  {
                    label: "Available",
                    dataField: "available",
                    dataType: "boolean"
                  }
                ]
              };
            }
          }
        );
      });
    }
  };
  </script>
  
  <style>
  body {
    height: 800px;
   
  }
  </style>