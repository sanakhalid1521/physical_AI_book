import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  docsSidebar: [
    {
      type: 'category',
      label: 'Introduction',
      items: [
        'chapters/introduction/foundations-of-physical-ai',
        'chapters/introduction/humanoid-robot-architecture',
        'chapters/introduction/simulation-environments'
      ],
      link: {
        type: 'doc',
        id: 'chapters/introduction/foundations-of-physical-ai',
      }
    },
    {
      type: 'category',
      label: 'Perception Systems',
      items: [
        'chapters/perception/sensor-integration',
        'chapters/perception/computer-vision-for-robotics',
        'chapters/perception/multi-modal-perception'
      ],
      link: {
        type: 'doc',
        id: 'chapters/perception/sensor-integration',
      }
    },
    {
      type: 'category',
      label: 'Decision Making and Control',
      items: [
        'chapters/control/motion-planning',
        'chapters/control/behavioral-control',
        'chapters/control/learning-based-control'
      ],
      link: {
        type: 'doc',
        id: 'chapters/control/motion-planning',
      }
    },
    {
      type: 'category',
      label: 'AI Integration and Intelligence',
      items: [
        'chapters/intelligence/planning-and-reasoning',
        'chapters/intelligence/human-robot-interaction',
        'chapters/intelligence/autonomous-learning'
      ],
      link: {
        type: 'doc',
        id: 'chapters/intelligence/planning-and-reasoning',
      }
    },
    {
      type: 'category',
      label: 'Advanced Applications and Integration',
      items: [
        'chapters/applications/real-world-deployment',
        'chapters/applications/specialized-applications',
        'chapters/applications/future-directions'
      ],
      link: {
        type: 'doc',
        id: 'chapters/applications/real-world-deployment',
      }
    }
  ],
};

export default sidebars;
