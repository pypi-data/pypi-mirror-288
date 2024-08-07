import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { requestAPI } from './handler';

/**
 * Initialization data for the @g2nb/nbtools extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: '@g2nb/nbtools:plugin',
  description: 'Framework for creating user-friendly Jupyter notebooks, accessible to both programming and non-programming users alike.',
  autoStart: true,
  optional: [ISettingRegistry],
  activate: (app: JupyterFrontEnd, settingRegistry: ISettingRegistry | null) => {
    console.log('JupyterLab extension @g2nb/nbtools is activated!');

    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          console.log('@g2nb/nbtools settings loaded:', settings.composite);
        })
        .catch(reason => {
          console.error('Failed to load settings for @g2nb/nbtools.', reason);
        });
    }

    requestAPI<any>('get-example')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The nbtools server extension appears to be missing.\n${reason}`
        );
      });
  }
};

export default plugin;
