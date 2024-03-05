<template>
  <div class="boolean-search-container">
    <div class="boolean-search">
    <div v-for="(condition, index) in conditions" :key="index" class="condition">
      <template v-if="index === 0">
          <select v-model="condition.type">
            <option value="free">Free Text</option>
            <option value="prox">Proximity Search</option>
          </select>
          <!-- Conditionally render input fields based on the selected type -->
          <template v-if="condition.type === 'free'">
            <input type="text" v-model="condition.value" placeholder="Free Text">
          </template>
          <template v-else-if="condition.type === 'prox'">
            <input type="text" v-model="condition.value" placeholder="Free Text">
            <input type="text" v-model="condition.value" placeholder="Free Text">
            <input type="number" v-model="condition.distance" placeholder="Distance">
          </template>
        </template>
        <template v-else>
          <!-- Render both field dropdown and value input for other rows -->
          <select v-model="condition.logic" >
            <option value="AND">AND</option>
            <option value="OR">OR</option>
            <option value="AND_NOT">AND NOT</option>
            <option value="OR_NOT">OR NOT</option>
          </select>
          <select v-model="condition.type">
            <option value="free">Free Text</option>
            <option value="prox">Proximity Search</option>
          </select>
          <!-- Conditionally render input fields based on the selected type -->
          <template v-if="condition.type === 'free'">
            <input type="text" v-model="condition.value" placeholder="Free Text">
          </template>
          <template v-else-if="condition.type === 'prox'">
            <input type="text" v-model="condition.value1" placeholder="Free Text">
            <input type="text" v-model="condition.value2" placeholder="Free Text">
            <input type="number" v-model="condition.distance" placeholder="Distance">
          </template>
          <button @click="removeCondition(index)">-</button>
        </template>
      </div>
      <button @click="addCondition">Add Condition</button>
      <button @click="constructQuery" class="button-primary">Search</button> <!-- Add button-primary class -->
    </div>
  </div>
  
</template>

<script>
export default {
  name: 'BooleanSearch',
  data() {
    return {
      conditions: [{ logic: 'AND', type:'free', value: '' }] // Set default condition to "AND"
    };
  },
  methods: {
    addCondition() {
      this.conditions.push({ logic: 'AND', type:'free', value: '' });
    },
    removeCondition(index) {
      this.conditions.splice(index, 1);
    },
    constructQuery() {
      const query = this.conditions.map(condition => `${condition.field}:${condition.value}`).join(' AND ');
      this.$emit('query-constructed', query);
    }
  }
};
</script>

<style scoped>

.boolean-search-container {
  width: 100%;
  max-width: 500px;
  background: rgba(25, 25, 25, 0.15);
  display: flex;
  align-items: center;
  border-radius: 20px;
  padding: 20px 20px 10px 20px;
  backdrop-filter: blur(4px) saturate(180%);
  margin: 20px auto; /* Center align the search bar */
  justify-content: center; /* Center align horizontally */
}

.button, button, input[type=button], input[type=reset], input[type=submit] {
  display: inline-block;
  height: 38px;
  padding: 0 30px;
  color: #555;
  text-align: center;
  font-size: 11px;
  font-weight: 600;
  line-height: 38px;
  letter-spacing: .1rem;
  text-transform: uppercase;
  text-decoration: none;
  white-space: nowrap;
  background-color: transparent;
  border-radius: 4px;
  border: 1px solid #bbb;
  cursor: pointer;
  box-sizing: border-box;
}

.boolean-search-container .logic-dropdown {
  width: 150px; /* Adjust the width as needed */
}

.button:focus, .button:hover, button:focus, button:hover, input[type=button]:focus, input[type=button]:hover, input[type=reset]:focus, input[type=reset]:hover, input[type=submit]:focus, input[type=submit]:hover {
  color: #333;
  border-color: #888;
  outline: 0;
}

.button.button-primary, button.button-primary, input[type=button].button-primary, input[type=reset].button-primary, input[type=submit].button-primary {
  color: #FFF;
  background-color: rgb(67, 100, 152);
  border-color: rgb(67, 100, 152);
}

.button.button-primary:focus, .button.button-primary:hover, button.button-primary:focus, button.button-primary:hover, input[type=button].button-primary:focus, input[type=button].button-primary:hover, input[type=reset].button-primary:focus, input[type=reset].button-primary:hover, input[type=submit].button-primary:focus, input[type=submit].button-primary:hover {
  color: #FFF;
  background-color: rgb(67, 100, 152);
  border-color: rgb(67, 100, 152);
}

.input[type=email], input[type=number], input[type=password], input[type=search], input[type=tel], input[type=text], input[type=url], select, textarea {
  height: 38px;
  padding: 6px 10px;
  background-color: #fff;
  border: 1px solid #D1D1D1;
  border-radius: 4px;
  box-shadow: none;
  box-sizing: border-box;
}

input[type=email], input[type=number], input[type=password], input[type=search], input[type=tel], input[type=text], input[type=url], textarea {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}

textarea {
  min-height: 65px;
  padding-top: 6px;
  padding-bottom: 6px;
}

input[type=email]:focus, input[type=number]:focus, input[type=password]:focus, input[type=search]:focus, input[type=tel]:focus, input[type=text]:focus, input[type=url]:focus, select:focus, textarea:focus {
  border: 1px solid #33C3F0;
  outline: 0;
}

.label, legend {
  display: block;
  margin-bottom: .5rem;
  font-weight: 600;
}

fieldset {
  padding: 0;
  border-width: 0;
}

input[type=checkbox], input[type=radio] {
  display: inline;
}

.label>.label-body {
  display: inline-block;
  margin-left: .5rem;
  font-weight: 400;
}

</style>