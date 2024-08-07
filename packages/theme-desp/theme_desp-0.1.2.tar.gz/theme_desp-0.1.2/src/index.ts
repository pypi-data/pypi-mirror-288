import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

import despLogo from '../style/desp-logo.png';
import destinationEarthLogo from '../style/destination-earth.png';
import fundedByEULogo from '../style/funded-by-EU.png';
import implementedByLogo from '../style/implemented-by.png';
import ecmwfLogo from '../style/ecmwf.png';
import esaLogo from '../style/esa.png';
import eumetsatLogo from '../style/eumetsat.png';

/**
 * Creates a logo, an 'img' element wrapped by a 'a' element
 */
const createLogo = (logoSrc: string, maxHeight: string, href?: string) => {
  const logoContainer = document.createElement('a');
  logoContainer.href = href || '#';
  logoContainer.target = '_blank';

  const logo = document.createElement('img');
  logo.style.width = 'auto';
  logo.style.maxHeight = maxHeight;
  logo.style.margin = '5px';
  logo.src = logoSrc;

  logoContainer.appendChild(logo);
  return logoContainer;
};

/**
 * Initialization data for the theme-desp extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'theme-desp:plugin',
  description: 'A JupyterLab extension.',
  autoStart: true,
  requires: [IThemeManager],
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    let footerVisible = true;

    const showFooter = () => {
      const footer = document.createElement('div');
      footer.classList.add('desp-footer');

      const logo1 = createLogo(
        despLogo,
        '36px',
        'https://destination-earth.eu/'
      );
      const logo2 = createLogo(
        destinationEarthLogo,
        '40px',
        'https://destination-earth.eu/'
      );
      const logo3 = createLogo(
        fundedByEULogo,
        '40px',
        'https://european-union.europa.eu/'
      );
      const logo4 = createLogo(
        implementedByLogo,
        '40px',
        'https://european-union.europa.eu/'
      );
      const logo5 = createLogo(ecmwfLogo, '40px', 'https://www.ecmwf.int/');
      const logo6 = createLogo(esaLogo, '40px', 'https://www.esa.int/');
      const logo7 = createLogo(
        eumetsatLogo,
        '40px',
        'https://www.eumetsat.int/'
      );
      const closeIcon = document.createElement('span');
      closeIcon.textContent = 'x';

      footer.appendChild(logo1);
      footer.appendChild(logo2);
      footer.appendChild(logo3);
      footer.appendChild(logo4);
      footer.appendChild(logo5);
      footer.appendChild(logo6);
      footer.appendChild(logo7);
      footer.appendChild(closeIcon);

      closeIcon.addEventListener('click', () => {
        document.body.removeChild(footer);
        footerVisible = false;
        showReopenButton();
      });

      document.body.appendChild(footer);
      footerVisible = true;
    };

    const showReopenButton = () => {
      if (document.getElementById('desp-footer-open-button')) return;

      const reopenButton = document.createElement('img');
      reopenButton.id = 'desp-footer-open-button';
      reopenButton.src = despLogo;
      reopenButton.classList.add('desp-footer-open-button');

      reopenButton.addEventListener('click', () => {
        document.body.removeChild(reopenButton);
        showFooter();
      });

      document.body.appendChild(reopenButton);
    };

    if (footerVisible) {
      showFooter();
    } else {
      showReopenButton();
    }

    const style = 'theme-desp/index.css';
    console.log('JupyterLab extension theme-desp is activated!');

    manager.register({
      name: 'theme-desp',
      isLight: true,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default plugin;
