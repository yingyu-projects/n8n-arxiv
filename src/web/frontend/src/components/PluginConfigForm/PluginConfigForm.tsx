'use client';

import { useState, useEffect } from 'react';
import styles from './PluginConfigForm.module.scss';

interface PluginConfigFormProps {
  schema: Record<string, any>;
  initialValues?: Record<string, any>;
  onChange: (values: Record<string, any>) => void;
  errors?: Record<string, string>;
}

export default function PluginConfigForm({
  schema,
  initialValues = {},
  onChange,
  errors = {},
}: PluginConfigFormProps) {
  const [values, setValues] = useState<Record<string, any>>(() => {
    // Initialize with defaults from schema
    const defaults: Record<string, any> = {};
    const properties = schema.properties || {};

    Object.keys(properties).forEach((key) => {
      const prop = properties[key];
      if (initialValues[key] !== undefined) {
        defaults[key] = initialValues[key];
      } else if (prop.default !== undefined) {
        defaults[key] = prop.default;
      } else if (prop.type === 'boolean') {
        defaults[key] = false;
      } else if (prop.type === 'array') {
        defaults[key] = [];
      } else {
        defaults[key] = '';
      }
    });

    return defaults;
  });

  useEffect(() => {
    // Update values when initialValues change (e.g., when config is loaded from server)
    const properties = schema.properties || {};
    const updated: Record<string, any> = { ...values };

    Object.keys(properties).forEach((key) => {
      if (initialValues[key] !== undefined) {
        updated[key] = initialValues[key];
      }
    });

    setValues(updated);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [initialValues]);

  const handleChange = (key: string, value: any) => {
    const newValues = { ...values, [key]: value };
    setValues(newValues);
    onChange(newValues);
  };

  const renderField = (key: string, prop: any) => {
    const required = (schema.required || []).includes(key);
    const value = values[key] ?? '';
    const error = errors[key];
    const title = prop.title || key;
    const description = prop.description || '';

    switch (prop.type) {
      case 'string':
        if (prop.enum) {
          return (
            <div key={key} className={styles.field}>
              <label className={styles.label}>
                {title}
                {required && <span className={styles.required}>*</span>}
              </label>
              {description && <p className={styles.description}>{description}</p>}
              <select
                value={value}
                onChange={(e) => handleChange(key, e.target.value)}
                className={`${styles.input} ${error ? styles.inputError : ''}`}
              >
                <option value="">Select {title}</option>
                {prop.enum.map((option: string) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
              {error && <span className={styles.error}>{error}</span>}
            </div>
          );
        }
        return (
          <div key={key} className={styles.field}>
            <label className={styles.label}>
              {title}
              {required && <span className={styles.required}>*</span>}
            </label>
            {description && <p className={styles.description}>{description}</p>}
            <input
              type="text"
              value={value}
              onChange={(e) => handleChange(key, e.target.value)}
              className={`${styles.input} ${error ? styles.inputError : ''}`}
              placeholder={prop.placeholder || `Enter ${title.toLowerCase()}`}
            />
            {error && <span className={styles.error}>{error}</span>}
          </div>
        );

      case 'number':
      case 'integer':
        return (
          <div key={key} className={styles.field}>
            <label className={styles.label}>
              {title}
              {required && <span className={styles.required}>*</span>}
            </label>
            {description && <p className={styles.description}>{description}</p>}
            <input
              type="number"
              value={value}
              onChange={(e) =>
                handleChange(key, prop.type === 'integer' ? parseInt(e.target.value, 10) : parseFloat(e.target.value))
              }
              className={`${styles.input} ${error ? styles.inputError : ''}`}
              placeholder={prop.placeholder || `Enter ${title.toLowerCase()}`}
            />
            {error && <span className={styles.error}>{error}</span>}
          </div>
        );

      case 'boolean':
        return (
          <div key={key} className={styles.field}>
            <label className={styles.checkboxLabel}>
              <input
                type="checkbox"
                checked={value || false}
                onChange={(e) => handleChange(key, e.target.checked)}
                className={styles.checkbox}
              />
              <span>
                {title}
                {required && <span className={styles.required}>*</span>}
              </span>
            </label>
            {description && <p className={styles.description}>{description}</p>}
            {error && <span className={styles.error}>{error}</span>}
          </div>
        );

      default:
        return null;
    }
  };

  const properties = schema.properties || {};

  return (
    <div className={styles.form}>
      {Object.keys(properties).map((key) => renderField(key, properties[key]))}
    </div>
  );
}

