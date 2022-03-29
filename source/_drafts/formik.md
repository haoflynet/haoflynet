```javascript
import React from 'react';
import { Formik } from 'formik';
import * as Yup from "yup";
 
const SignupSchema = Yup.object().shape({
  name: Yup.string()
  .min(2, 'Too Short!')
  .max(70, 'Too Long!')
  .required('Required'),
  email: Yup.string()
  .email('Invalid email')
  .required('Required'),
});

const BasicExample = () => (
  <div>
    <h1>My Form</h1>
    <Formik
      initialValues={{ name: 'jared' }}
      validationSchema={SignupSchema}
      onSubmit={(values, actions) => {
        setTimeout(() => {
          alert(JSON.stringify(values, null, 2));
          actions.setSubmitting(false);
        }, 1000);
      }}
    >
      {props => (
        <form onSubmit={props.handleSubmit}>
          <input
            type="text"
            onChange={props.handleChange}
            onBlur={props.handleBlur}
            value={props.values.name}
            name="name"
          />
          {props.errors.name && <div id="feedback">{props.errors.name}</div>}
	         <ErrorMessage name="name" /> // 另外一种展示错误的方法
          <button type="submit">Submit</button>
        </form>
      )}
    </Formik>
  </div>
);
```

