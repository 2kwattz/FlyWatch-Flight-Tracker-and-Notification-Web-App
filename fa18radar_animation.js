import React, { useEffect, useRef } from 'react';
import { Animated, View, StyleSheet, Dimensions } from 'react-native';

const { width, height } = Dimensions.get('window');

const RadarAnimation = () => {
  const sweepAnim = useRef(new Animated.Value(0)).current; // Animation value for the sweep
  
  // Function to trigger the sweep animation
  const startRadarAnimation = () => {
    Animated.loop(
      Animated.timing(sweepAnim, {
        toValue: 1,
        duration: 4000, // Adjust sweep time to simulate a realistic radar sweep
        useNativeDriver: false,
      })
    ).start();
  };

  // Start animation on mount
  useEffect(() => {
    startRadarAnimation();
  }, []);

  // Interpolate sweepAnim to control the line position for rotating
  const rotationInterpolate = sweepAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'], // Rotate from 0deg to 360deg
  });

  return (
    <View style={styles.container}>
      <View style={styles.radarContainer}>
        {/* Static Radial Lines */}
        {Array.from({ length: 12 }).map((_, index) => (
          <View
            key={index}
            style={[
              styles.radialLine,
              {
                transform: [{ rotate: `${(360 / 12) * index}deg` }],
              },
            ]}
          />
        ))}

        {/* Static Concentric Circles */}
        <View style={styles.circle1} />
        <View style={styles.circle2} />
        <View style={styles.circle3} />
        
        {/* Static Horizontal and Vertical Dashes */}
        <View style={styles.topDash} />
        <View style={styles.bottomDash} />
        <View style={styles.leftDash} />
        <View style={styles.rightDash} />

        {/* Rotating Sweep Line */}
        <Animated.View
          style={[
            styles.sweepLine,
            { transform: [{ rotate: rotationInterpolate }] }, // Apply rotation animation to sweep line
          ]}
        />

        {/* Center Circle */}
        <View style={styles.centerCircle} />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'black', // Background to mimic radar environment
  },
  radarContainer: {
    width: 300, // Size of the radar (square)
    height: 300,
    backgroundColor: 'rgba(0, 255, 0, 0.1)', // Greenish background for the radar
    borderWidth: 1, // Single 1px border around the radar
    borderColor: '#00FF00', // Green radar border
    borderRadius: 150, // Circular radar
    position: 'relative',
    overflow: 'hidden', // To hide elements that go outside the circle
  },
  radialLine: {
    position: 'absolute',
    width: 2, // Thin line for radial lines
    height: '100%',
    backgroundColor: '#00FF00', // Green color for radial lines
    top: 0,
    left: '50%',
    marginLeft: -1, // To center the line
  },
  circle1: {
    position: 'absolute',
    width: 60,
    height: 60,
    borderRadius: 30,
    borderWidth: 2,
    borderColor: '#00FF00',
    top: '50%',
    left: '50%',
    marginLeft: -30, // To center the circle
    marginTop: -30,
  },
  circle2: {
    position: 'absolute',
    width: 120,
    height: 120,
    borderRadius: 60,
    borderWidth: 2,
    borderColor: '#00FF00',
    top: '50%',
    left: '50%',
    marginLeft: -60, // To center the circle
    marginTop: -60,
  },
  circle3: {
    position: 'absolute',
    width: 180,
    height: 180,
    borderRadius: 90,
    borderWidth: 2,
    borderColor: '#00FF00',
    top: '50%',
    left: '50%',
    marginLeft: -90, // To center the circle
    marginTop: -90,
  },
  topDash: {
    position: 'absolute',
    top: 0,
    left: 0,
    width: '100%',
    height: 4,
    backgroundColor: '#00FF00', // Green dashes on top
  },
  bottomDash: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    width: '100%',
    height: 4,
    backgroundColor: '#00FF00', // Green dashes on bottom
  },
  leftDash: {
    position: 'absolute',
    top: 0,
    left: 0,
    width: 4,
    height: '100%',
    backgroundColor: '#00FF00', // Green dashes on left
  },
  rightDash: {
    position: 'absolute',
    top: 0,
    right: 0,
    width: 4,
    height: '100%',
    backgroundColor: '#00FF00', // Green dashes on right
  },
  sweepLine: {
    position: 'absolute',
    width: 4, // Thin line for the sweep
    height: '100%',
    backgroundColor: '#00FF00', // Green color for the sweep line
    top: 0,
    left: '50%',
    marginLeft: -2, // Center the line
  },
  centerCircle: {
    position: 'absolute',
    width: 20,
    height: 20,
    borderRadius: 10,
    backgroundColor: '#00FF00', // Small green center circle
    top: '50%',
    left: '50%',
    marginLeft: -10, // To center the circle
    marginTop: -10,
  },
});

export default RadarAnimation;
