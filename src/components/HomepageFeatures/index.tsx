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
    title: 'Module 1: ROS 2 Foundations',
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
    title: 'Module 2: Digital Twins & Simulation',
    icon: '🖥️',
    description: (
      <>
        Create virtual replicas of physical systems. Learn URDF modeling,
        Gazebo simulation environments, and launch file orchestration.
        Develop and validate robotic systems in safe, virtual workspaces.
      </>
    ),
  },
  {
    title: 'Module 3: Physical AI & VLA Models',
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
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <span className={styles.featureIcon} role="img">{icon}</span>
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
