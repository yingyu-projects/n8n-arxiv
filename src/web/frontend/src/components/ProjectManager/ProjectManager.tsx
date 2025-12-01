'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useProjects } from '@/hooks/useProjects';
import styles from './ProjectManager.module.scss';

export default function ProjectManager() {
  const { projects, loading, error, createProject, updateProject, deleteProject } = useProjects();
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [creating, setCreating] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
  });

  const handleCreate = async () => {
    if (!formData.name.trim()) {
      alert('Project name is required');
      return;
    }
    setCreating(true);
    try {
      await createProject({
        name: formData.name,
        description: formData.description || null,
      });
      setShowCreateForm(false);
      setFormData({ name: '', description: '' });
    } catch (err: any) {
      alert(err.message || 'Failed to create project');
    } finally {
      setCreating(false);
    }
  };

  const handleUpdate = async (id: string) => {
    if (!formData.name.trim()) {
      alert('Project name is required');
      return;
    }
    try {
      await updateProject(id, {
        name: formData.name,
        description: formData.description || null,
      });
      setEditingId(null);
      setFormData({ name: '', description: '' });
    } catch (err: any) {
      alert(err.message || 'Failed to update project');
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this project?')) return;
    try {
      await deleteProject(id);
    } catch (err: any) {
      alert(err.message || 'Failed to delete project');
    }
  };

  const startEdit = (project: { id: string; name: string; description: string | null }) => {
    setEditingId(project.id);
    setFormData({
      name: project.name,
      description: project.description || '',
    });
    setShowCreateForm(false);
  };

  const cancelEdit = () => {
    setEditingId(null);
    setFormData({ name: '', description: '' });
  };

  return (
    <div className={styles.projectManager}>
      <div className={styles.header}>
        <h2>Projects</h2>
        <button
          onClick={() => {
            setShowCreateForm(!showCreateForm);
            setEditingId(null);
            setFormData({ name: '', description: '' });
          }}
          className={styles.createButton}
        >
          {showCreateForm ? 'Cancel' : 'Create Project'}
        </button>
      </div>

      {showCreateForm && (
        <div className={styles.createForm}>
          <h3>Create New Project</h3>
          <input
            type="text"
            placeholder="Project name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            className={styles.input}
          />
          <textarea
            placeholder="Description (optional)"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            className={styles.textarea}
          />
          <button onClick={handleCreate} disabled={creating} className={styles.submitButton}>
            {creating ? 'Creating...' : 'Create'}
          </button>
        </div>
      )}

      {loading && <div className={styles.loading}>Loading projects...</div>}
      {error && <div className={styles.error}>{error.message}</div>}

      {!loading && !error && projects.length === 0 && (
        <div className={styles.empty}>No projects found. Create one to get started.</div>
      )}

      {!loading && !error && projects.length > 0 && (
        <div className={styles.projects}>
          {projects.map((project) => (
            <div key={project.id} className={styles.projectItem}>
              {editingId === project.id ? (
                <div className={styles.editForm}>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className={styles.input}
                  />
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    className={styles.textarea}
                  />
                  <div className={styles.editActions}>
                    <button onClick={() => handleUpdate(project.id)} className={styles.saveButton}>
                      Save
                    </button>
                    <button onClick={cancelEdit} className={styles.cancelButton}>
                      Cancel
                    </button>
                  </div>
                </div>
              ) : (
                <>
                  <Link href={`/projects/${project.id}`} className={styles.projectInfo}>
                    <h3>{project.name}</h3>
                    {project.description && <p>{project.description}</p>}
                    <div className={styles.meta}>
                      <span>Created: {new Date(project.created_at).toLocaleDateString()}</span>
                    </div>
                  </Link>
                  <div className={styles.actions}>
                    <button
                      onClick={(e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        startEdit(project);
                      }}
                      className={styles.editButton}
                    >
                      Edit
                    </button>
                    <button
                      onClick={(e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        handleDelete(project.id);
                      }}
                      className={styles.deleteButton}
                    >
                      Delete
                    </button>
                  </div>
                </>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

