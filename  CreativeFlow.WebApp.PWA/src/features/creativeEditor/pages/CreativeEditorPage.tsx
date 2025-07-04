import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useDocumentTitle } from '@/shared/hooks/useDocumentTitle';
import styles from './CreativeEditorPage.module.css';
import { useCreativeEditorStore } from '@/app/store';
import { useProjectStore } from '@/app/store';

// Placeholder components for the editor layout
const Canvas = () => <div className={styles.canvasPlaceholder}>Canvas Area</div>;
const Toolbar = () => <div className={styles.toolbarPlaceholder}>Toolbar</div>;
const PropertiesPanel = () => <div className={styles.propertiesPanelPlaceholder}>Properties Panel</div>;
const AssetPicker = () => <div className={styles.assetPickerPlaceholder}>Asset Picker</div>;
const CollaborationBar = () => <div className={styles.collaborationBarPlaceholder}>Collaborators</div>;

/**
 * The main page component for the Creative Editor workspace.
 * This component orchestrates the entire editor UI, including the canvas,
 * toolbars, and property panels. It's responsible for fetching the asset
 * being edited and setting up the editor state.
 *
 * @returns {React.ReactElement} The rendered creative editor page.
 */
const CreativeEditorPage: React.FC = () => {
  const { assetId } = useParams<{ assetId: string }>();
  const { t } = useTranslation('editor');
  
  const { fetchProjectDetails } = useProjectStore(state => ({ fetchProjectDetails: state.fetchProjectDetails }));
  const { asset, project } = useProjectStore(state => ({ asset: state.currentAsset, project: state.currentProject }));
  
  const { setCanvasState, resetEditorState } = useCreativeEditorStore(state => ({
    setCanvasState: state.setCanvasState,
    resetEditorState: state.resetEditorState
  }));

  // Set document title based on project/asset name
  const pageTitle = project ? `${t('pageTitle')} - ${project.name}` : t('pageTitle');
  useDocumentTitle(pageTitle);

  useEffect(() => {
    if (assetId) {
      // In a real app, you would fetch asset details, which would include project info
      // For now, let's assume assetId can be used to find project details
      // This logic should be improved with a proper API endpoint `GET /assets/:id`
      // which returns the asset and its parent project.
      console.log('Fetching details for asset:', assetId);
      // fetchProjectDetails(asset.projectId); // This assumes we have asset details first
    } else {
      // New asset, reset the editor state
      resetEditorState();
    }

    // Cleanup on unmount
    return () => {
      resetEditorState();
    };
  }, [assetId, fetchProjectDetails, resetEditorState]);

  // TODO: Add logic for initializing collaboration session with Y.js
  // const { provider } = useCollaboration(project?.id);

  return (
    <div className={styles.editorLayout}>
      <header className={styles.editorHeader}>
        <div className={styles.headerLeft}>
          {/* Breadcrumbs or Project Name */}
          <h2>{project?.name || t('newCreative')}</h2>
        </div>
        <div className={styles.headerCenter}>
          <Toolbar />
        </div>
        <div className={styles.headerRight}>
          <CollaborationBar />
          {/* Export/Save Buttons */}
        </div>
      </header>
      <main className={styles.editorMain}>
        <aside className={styles.leftPanel}>
          <AssetPicker />
        </aside>
        <div className={styles.canvasContainer}>
          <Canvas />
        </div>
        <aside className={styles.rightPanel}>
          <PropertiesPanel />
        </aside>
      </main>
    </div>
  );
};

export default CreativeEditorPage;