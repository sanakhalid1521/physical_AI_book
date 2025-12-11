import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '5ff'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '5ba'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'a2b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'c3c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '156'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '88c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '000'),
    exact: true
  },
  {
    path: '/index_old',
    component: ComponentCreator('/index_old', '042'),
    exact: true
  },
  {
    path: '/login',
    component: ComponentCreator('/login', 'f43'),
    exact: true
  },
  {
    path: '/markdown-page',
    component: ComponentCreator('/markdown-page', '3d7'),
    exact: true
  },
  {
    path: '/signup',
    component: ComponentCreator('/signup', '312'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', '86d'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', '7ea'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '634'),
            routes: [
              {
                path: '/docs/assessments/chapter-1-assessment',
                component: ComponentCreator('/docs/assessments/chapter-1-assessment', '492'),
                exact: true
              },
              {
                path: '/docs/assessments/chapter-2-assessment',
                component: ComponentCreator('/docs/assessments/chapter-2-assessment', '4ac'),
                exact: true
              },
              {
                path: '/docs/assessments/chapter-3-assessment',
                component: ComponentCreator('/docs/assessments/chapter-3-assessment', 'ac8'),
                exact: true
              },
              {
                path: '/docs/assessments/chapter-4-assessment',
                component: ComponentCreator('/docs/assessments/chapter-4-assessment', 'd34'),
                exact: true
              },
              {
                path: '/docs/assessments/chapter-5-assessment',
                component: ComponentCreator('/docs/assessments/chapter-5-assessment', '7c9'),
                exact: true
              },
              {
                path: '/docs/assessments/comprehensive-review',
                component: ComponentCreator('/docs/assessments/comprehensive-review', '9b1'),
                exact: true
              },
              {
                path: '/docs/assessments/exercise-reproducibility',
                component: ComponentCreator('/docs/assessments/exercise-reproducibility', 'b64'),
                exact: true
              },
              {
                path: '/docs/assessments/features-verification',
                component: ComponentCreator('/docs/assessments/features-verification', '571'),
                exact: true
              },
              {
                path: '/docs/assessments/troubleshooting-guide',
                component: ComponentCreator('/docs/assessments/troubleshooting-guide', '52f'),
                exact: true
              },
              {
                path: '/docs/chapters/applications/future-directions',
                component: ComponentCreator('/docs/chapters/applications/future-directions', '11d'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/chapters/applications/real-world-deployment',
                component: ComponentCreator('/docs/chapters/applications/real-world-deployment', 'fbc'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/chapters/applications/specialized-applications',
                component: ComponentCreator('/docs/chapters/applications/specialized-applications', '67d'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/chapters/control/behavioral-control',
                component: ComponentCreator('/docs/chapters/control/behavioral-control', '617'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/chapters/control/learning-based-control',
                component: ComponentCreator('/docs/chapters/control/learning-based-control', '0d2'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/chapters/control/motion-planning',
                component: ComponentCreator('/docs/chapters/control/motion-planning', 'c59'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/chapters/intelligence/autonomous-learning',
                component: ComponentCreator('/docs/chapters/intelligence/autonomous-learning', 'cad'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/chapters/intelligence/human-robot-interaction',
                component: ComponentCreator('/docs/chapters/intelligence/human-robot-interaction', '915'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/chapters/intelligence/planning-and-reasoning',
                component: ComponentCreator('/docs/chapters/intelligence/planning-and-reasoning', '370'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/chapters/introduction/foundations-of-physical-ai',
                component: ComponentCreator('/docs/chapters/introduction/foundations-of-physical-ai', '9c4'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/chapters/introduction/humanoid-robot-architecture',
                component: ComponentCreator('/docs/chapters/introduction/humanoid-robot-architecture', '170'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/chapters/introduction/simulation-environments',
                component: ComponentCreator('/docs/chapters/introduction/simulation-environments', 'eba'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/chapters/perception/computer-vision-for-robotics',
                component: ComponentCreator('/docs/chapters/perception/computer-vision-for-robotics', '657'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/chapters/perception/multi-modal-perception',
                component: ComponentCreator('/docs/chapters/perception/multi-modal-perception', 'd63'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/chapters/perception/sensor-integration',
                component: ComponentCreator('/docs/chapters/perception/sensor-integration', '6c9'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/course-materials/course-syllabus-template',
                component: ComponentCreator('/docs/course-materials/course-syllabus-template', '8b1'),
                exact: true
              },
              {
                path: '/docs/educator-guides/applications/educator-guide',
                component: ComponentCreator('/docs/educator-guides/applications/educator-guide', '18a'),
                exact: true
              },
              {
                path: '/docs/educator-guides/control/educator-guide',
                component: ComponentCreator('/docs/educator-guides/control/educator-guide', '5a3'),
                exact: true
              },
              {
                path: '/docs/educator-guides/intelligence/educator-guide',
                component: ComponentCreator('/docs/educator-guides/intelligence/educator-guide', 'f69'),
                exact: true
              },
              {
                path: '/docs/educator-guides/introduction/educator-guide',
                component: ComponentCreator('/docs/educator-guides/introduction/educator-guide', '497'),
                exact: true
              },
              {
                path: '/docs/educator-guides/perception/educator-guide',
                component: ComponentCreator('/docs/educator-guides/perception/educator-guide', '462'),
                exact: true
              },
              {
                path: '/docs/exercises/applications/exercise-5.1-real-world-deployment',
                component: ComponentCreator('/docs/exercises/applications/exercise-5.1-real-world-deployment', 'a65'),
                exact: true
              },
              {
                path: '/docs/exercises/applications/exercise-5.2-specialized-applications',
                component: ComponentCreator('/docs/exercises/applications/exercise-5.2-specialized-applications', '656'),
                exact: true
              },
              {
                path: '/docs/exercises/applications/exercise-5.3-future-directions',
                component: ComponentCreator('/docs/exercises/applications/exercise-5.3-future-directions', '6e1'),
                exact: true
              },
              {
                path: '/docs/exercises/control/exercise-3.1-motion-planning',
                component: ComponentCreator('/docs/exercises/control/exercise-3.1-motion-planning', 'c00'),
                exact: true
              },
              {
                path: '/docs/exercises/control/exercise-3.2-behavioral-control',
                component: ComponentCreator('/docs/exercises/control/exercise-3.2-behavioral-control', '672'),
                exact: true
              },
              {
                path: '/docs/exercises/control/exercise-3.3-learning-based-control',
                component: ComponentCreator('/docs/exercises/control/exercise-3.3-learning-based-control', '94f'),
                exact: true
              },
              {
                path: '/docs/exercises/intelligence/exercise-4.1-planning-and-reasoning',
                component: ComponentCreator('/docs/exercises/intelligence/exercise-4.1-planning-and-reasoning', 'c83'),
                exact: true
              },
              {
                path: '/docs/exercises/intelligence/exercise-4.2-human-robot-interaction',
                component: ComponentCreator('/docs/exercises/intelligence/exercise-4.2-human-robot-interaction', '77c'),
                exact: true
              },
              {
                path: '/docs/exercises/intelligence/exercise-4.3-autonomous-learning',
                component: ComponentCreator('/docs/exercises/intelligence/exercise-4.3-autonomous-learning', '647'),
                exact: true
              },
              {
                path: '/docs/exercises/introduction/',
                component: ComponentCreator('/docs/exercises/introduction/', '3a3'),
                exact: true
              },
              {
                path: '/docs/exercises/introduction/exercise-1.1-basic-concepts',
                component: ComponentCreator('/docs/exercises/introduction/exercise-1.1-basic-concepts', '26a'),
                exact: true
              },
              {
                path: '/docs/exercises/introduction/exercise-1.2-robot-architecture',
                component: ComponentCreator('/docs/exercises/introduction/exercise-1.2-robot-architecture', 'b66'),
                exact: true
              },
              {
                path: '/docs/exercises/introduction/exercise-1.3-simulation-setup',
                component: ComponentCreator('/docs/exercises/introduction/exercise-1.3-simulation-setup', '732'),
                exact: true
              },
              {
                path: '/docs/exercises/perception/exercise-2.1-sensor-integration',
                component: ComponentCreator('/docs/exercises/perception/exercise-2.1-sensor-integration', '4bf'),
                exact: true
              },
              {
                path: '/docs/exercises/perception/exercise-2.2-computer-vision',
                component: ComponentCreator('/docs/exercises/perception/exercise-2.2-computer-vision', 'be1'),
                exact: true
              },
              {
                path: '/docs/exercises/perception/exercise-2.3-multi-modal-perception',
                component: ComponentCreator('/docs/exercises/perception/exercise-2.3-multi-modal-perception', 'a6c'),
                exact: true
              },
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', '853'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/congratulations',
                component: ComponentCreator('/docs/tutorial-basics/congratulations', '70e'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/create-a-blog-post',
                component: ComponentCreator('/docs/tutorial-basics/create-a-blog-post', '315'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/create-a-document',
                component: ComponentCreator('/docs/tutorial-basics/create-a-document', 'f86'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/create-a-page',
                component: ComponentCreator('/docs/tutorial-basics/create-a-page', '9f6'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/deploy-your-site',
                component: ComponentCreator('/docs/tutorial-basics/deploy-your-site', 'b91'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/markdown-features',
                component: ComponentCreator('/docs/tutorial-basics/markdown-features', '272'),
                exact: true
              },
              {
                path: '/docs/tutorial-extras/manage-docs-versions',
                component: ComponentCreator('/docs/tutorial-extras/manage-docs-versions', 'a34'),
                exact: true
              },
              {
                path: '/docs/tutorial-extras/translate-your-site',
                component: ComponentCreator('/docs/tutorial-extras/translate-your-site', '739'),
                exact: true
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', 'fd5'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
