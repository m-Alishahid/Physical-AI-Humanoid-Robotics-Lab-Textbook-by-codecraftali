import {themes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: '🤖 Physical AI & Humanoid Robotics Lab Textbook',
  tagline: 'Master ROS 2, Digital Twins, NVIDIA Isaac & Humanoid AI Systems',
  favicon: 'img/favicon.svg',
  url: 'https://physical-ai-lab.vercel.app/',
  baseUrl: '/',
  organizationName: 'codecraftali',
  projectName: 'Physical-AI-Humanoid-Robotics-Lab-Textbook-by-codecraftali',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  i18n: {defaultLocale: 'en', locales: ['en']},
  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: 'docs',
          path: 'docs',
          showLastUpdateTime: true,
          editUrl: 'https://github.com/codecraftali/Physical-AI-Humanoid-Robotics-Lab-Textbook-by-codecraftali/edit/main/',
        },
        blog: false,
        theme: {customCss: './src/css/custom.css'},
      },
    ],
  ],
  themeConfig: {
    navbar: {
      title: '🤖 Physical AI & Humanoid Robotics',
      logo: {alt: 'Robot Logo', src: 'img/logo.svg'},
      items: [
        {
          type: 'doc',
          docId: 'index', // The ID of the doc to link to (your intro page)
          position: 'left',
          label: '📚 Textbook',
        
        },
        {href: 'https://github.com/codecraftali/Physical-AI-Humanoid-Robotics-Lab-Textbook-by-codecraftali', label: 'GitHub', position: 'right'},
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Textbook',
          items: [
            {label: 'Introduction', to: '/docs'},
            {label: 'Setup Guides', to: '/docs/digital-twin-workstation'},
            {label: 'Module 1: ROS 2', to: '/docs/chapter1-introduction-to-ros2'},
          ],
        },
        {
          title: 'Resources',
          items: [
            {label: 'ROS 2 Docs', href: 'https://docs.ros.org'},
            {label: 'NVIDIA Isaac', href: 'https://developer.nvidia.com/isaac'},
            {label: 'Digital Twin Guide', href: 'https://www.autodesk.com/solutions/digital-twin'},
          ],
        },
        {
          title: 'Community',
          items: [
            {label: 'GitHub', href: 'https://github.com/codecraftali'},
            {label: 'Discord', href: 'https://discord.gg/robotics'},
            {label: 'Contact', href: 'mailto:contact@example.com'},
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Lab Textbook. All rights reserved.`,
    },
    prism: {
      theme: themes.dracula,
      additionalLanguages: ['python', 'cpp', 'bash', 'yaml', 'json', 'docker'],
    },
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
  },
};

export default config;
