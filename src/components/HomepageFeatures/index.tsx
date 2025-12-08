import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  icon: string;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Module 1: ROS 2 Fundamentals',
    icon: '🤖',
    description: (
      <>
        Master the Robot Operating System 2 architecture. Explore nodes, topics,
        services, actions, and parameters. Build robust robotic applications with
        industry-standard middleware and communication protocols.
      </>
    ),
  },
  {
    title: 'Module 2: Digital Twins',
    icon: '🔄',
    description: (
      <>
        Create virtual replicas of physical systems. Learn URDF modeling,
        Gazebo simulation environments, and launch file orchestration.
        Develop and validate robotic systems in safe, virtual workspaces.
      </>
    ),
  },
  {
    title: 'Module 3: NVIDIA Isaac',
    icon: '🎮',
    description: (
      <>
        Dive into NVIDIA's robotics simulation platform. Master Isaac Sim,
        Isaac Gym, and Sim2Real pipelines. Build and train AI models in
        photorealistic virtual environments before deploying to physical robots.
      </>
    ),
  },
  {
    title: 'Module 4: VLA & Humanoids',
    icon: '🧠',
    description: (
      <>
        Advance into cutting-edge AI integration. Implement Vision-Language-Action
        (VLA) models for humanoid robots. Combine computer vision, natural language
        processing, and robotic control for intelligent, adaptive behaviors.
      </>
    ),
  },
];

function Feature({title, icon, description}: FeatureItem) {
  return (
    <div className={clsx('col col--3')}>
      <div className="text--center">
        <div className={styles.featureIcon} role="img" aria-label={title}>
          {icon}
        </div>
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}