'use client';

import { useConfig } from '@/hooks/useConfig';
import { useProjectContext } from '@/hooks/useProjectContext';
import styles from './Config.module.scss';

export default function Config() {
  const { projectId } = useProjectContext();
  const {
    categories,
    newCategories,
    updateCategory,
    summarizePrompt,
    setSummarizePrompt,
    loading,
    saving,
    savingPrompt,
    error,
    saveCategories,
    saveSummarizePrompt,
    addCategory,
    removeCategory,
  } = useConfig();

  return (
    <div className={styles.config}>
      <h2>Configuration</h2>

      <div className={styles.section}>
        <h3>Categories</h3>
        <div className={styles.currentCategories}>
          <h4>Current Categories</h4>
          {loading ? (
            <div>Loading...</div>
          ) : categories.length === 0 ? (
            <div className={styles.empty}>No categories configured</div>
          ) : (
            <ul className={styles.categoryList}>
              {categories.map((cat) => (
                <li key={cat.id}>
                  {cat.name} ({cat.num_papers} papers)
                  {!cat.enabled && (
                    <span className={styles.disabled}> (disabled)</span>
                  )}
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className={styles.newCategories}>
          <h4>Update Categories</h4>
          {newCategories.map((category, index) => (
            <div key={index} className={styles.categoryInputGroup}>
              <input
                value={category}
                onChange={(e) => updateCategory(index, e.target.value)}
                type="text"
                placeholder="e.g., cs.AI"
                className={styles.categoryInput}
              />
              <button
                onClick={() => removeCategory(index)}
                type="button"
                className={styles.removeBtn}
                disabled={newCategories.length === 1}
              >
                Remove
              </button>
            </div>
          ))}
          <button onClick={addCategory} type="button" className={styles.addBtn}>
            Add Category
          </button>
          <button
            onClick={saveCategories}
            disabled={saving}
            className={styles.saveBtn}
          >
            {saving ? 'Saving...' : 'Save Categories'}
          </button>
        </div>
      </div>

      <div className={styles.section}>
        <h3>Summarize Prompt</h3>
        <div className={styles.promptSection}>
          <textarea
            value={summarizePrompt}
            onChange={(e) => setSummarizePrompt(e.target.value)}
            className={styles.promptTextarea}
            placeholder="Enter the summarize prompt..."
            rows={20}
          />
          <button
            onClick={saveSummarizePrompt}
            disabled={savingPrompt}
            className={styles.saveBtn}
          >
            {savingPrompt ? 'Saving...' : 'Save Prompt'}
          </button>
        </div>
      </div>

      {error && <div className={styles.error}>{error}</div>}
    </div>
  );
}

