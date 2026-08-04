import React, { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import * as THREE from 'three';

function Helix({ matchedCount = 5, missingCount = 3 }) {
  const groupRef = useRef(null);
  
  const numPoints = 26;
  const data = useMemo(() => {
    const points = [];
    const rungs = [];
    
    for (let i = 0; i < numPoints; i++) {
      const alpha = (i / numPoints) * Math.PI * 4; 
      const y = (i / numPoints) * 5.5 - 2.75; 
      const radius = 1.1;
      
      const x1 = Math.cos(alpha) * radius;
      const z1 = Math.sin(alpha) * radius;
      
      const x2 = Math.cos(alpha + Math.PI) * radius;
      const z2 = Math.sin(alpha + Math.PI) * radius;
      
      points.push({ pos: [x1, y, z1], id: `a-${i}` });
      points.push({ pos: [x2, y, z2], id: `b-${i}` });
      
      let isMatch = true;
      if (i % 3 === 0 && rungs.length < missingCount) {
        isMatch = false;
      }
      
      rungs.push({
        p1: [x1, y, z1],
        p2: [x2, y, z2],
        isMatch
      });
    }
    
    return { points, rungs };
  }, [matchedCount, missingCount]);

  useFrame(({ clock }) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = clock.elapsedTime * 0.35;
      groupRef.current.rotation.x = Math.sin(clock.elapsedTime * 0.08) * 0.08;
    }
  });

  return (
    <group ref={groupRef}>
      {/* Helix spheres - precision nodes */}
      {data.points.map((pt) => (
        <mesh key={pt.id} position={pt.pos}>
          <sphereGeometry args={[0.045, 12, 12]} />
          <meshBasicMaterial color="#ffffff" transparent opacity={0.65} />
        </mesh>
      ))}

      {/* Rung connectors - clinical thin segments */}
      {data.rungs.map((rung, idx) => {
        const p1 = new THREE.Vector3(...rung.p1);
        const p2 = new THREE.Vector3(...rung.p2);
        const distance = p1.distanceTo(p2);
        const position = p1.clone().add(p2).multiplyScalar(0.5);
        
        const direction = p2.clone().sub(p1).normalize();
        const arrow = new THREE.ArrowHelper(direction, p1);
        const rotation = arrow.rotation.clone();
        
        return (
          <mesh key={idx} position={position} rotation={rotation}>
            <cylinderGeometry args={[0.01, 0.01, distance, 6]} />
            <meshBasicMaterial 
              color={rung.isMatch ? "#10b981" : "#f43f5e"} 
              transparent 
              opacity={0.6} 
            />
          </mesh>
        );
      })}
    </group>
  );
}

export default function DnaHelix({ matchedCount, missingCount }) {
  return (
    <div className="h-[210px] w-full relative">
      <Canvas camera={{ position: [0, 0, 5], fov: 50 }} gl={{ antialias: true, alpha: true }}>
        <ambientLight intensity={0.6} />
        <pointLight position={[10, 10, 10]} />
        <Helix matchedCount={matchedCount} missingCount={missingCount} />
      </Canvas>
      <div className="absolute bottom-1 left-1/2 transform -translate-x-1/2 flex items-center gap-3 text-[9px] font-mono text-zinc-500 bg-zinc-950 border border-zinc-900 px-3 py-0.5 rounded-md">
        <span className="flex items-center gap-1.5"><span className="h-1.5 w-1.5 rounded-full bg-emerald-400"></span>Match</span>
        <span className="flex items-center gap-1.5"><span className="h-1.5 w-1.5 rounded-full bg-rose-400"></span>Gap</span>
      </div>
    </div>
  );
}
