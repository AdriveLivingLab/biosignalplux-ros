#include <ros/ros.h>
#include "std_msgs/String.h"

// Includes to match the biosignal frame definition
#include "std_msgs/Int64MultiArray.h"
#include "std_msgs/UInt8MultiArray.h"

#include <sstream>
#include <string>
#include "biosignalplux/biosignal.h"

#include "../include/Linux_ARM_64/plux.h"
#include "../include/simpleDev.h"

int main(int argc, char **argv)
{

  ros::init(argc, argv, "biosignal");
  ros::NodeHandle nh("~");
  
  std::string sMAC; 
  int nChannels, nFrequency; 

  
  if (!nh.getParam("mac_address", sMAC))
  {
	ROS_WARN("Missing MAC adress! (see biosignalplux.launch file!)");
  }

  if (!nh.getParam("frequency", nFrequency))
  {
        ROS_WARN("Missing device sample frequency! (see biosignalplux.launch file!)");
  }

  ros::Publisher chatter_pub = nh.advertise<biosignalplux::biosignal>("biosignalplux", 10);

    
  // Init msg  
  biosignalplux::biosignal oBiosig; 
  std_msgs::UInt8MultiArray aiBioSignalDigital;
  aiBioSignalDigital.data.resize(4); // Up to 4 digital outputs

  std_msgs::Int64MultiArray aiBioSignalAnalog; 
  aiBioSignalAnalog.data.resize(9); // seq + 8 channels

  SimpleDev dev(sMAC);
  
  dev.start(nFrequency, {1, 2, 3, 4, 5, 6, 7, 8}); 

  dev.trigger(false);

  SimpleDev::VFrame frames(1); // initialize the frames vector with x frames (From simpleDev cpp)

  while (ros::ok())
  {
	// Reading the data from device 

	dev.read(frames);
	const SimpleDev::Frame &f = frames[0];
    	oBiosig.header.stamp = ros::Time::now(); 
    	oBiosig.analog_1 = f.analog[0];
    	oBiosig.analog_2 = f.analog[1];
    	oBiosig.analog_3 = f.analog[2]; 
    	oBiosig.analog_4 = f.analog[3]; 
    	oBiosig.analog_5 = f.analog[4];
    	oBiosig.analog_6 = f.analog[5];
    	oBiosig.analog_7 = f.analog[6];
    	oBiosig.analog_8 = f.analog[7]; 
    	oBiosig.sequence = f.seq; 

    	chatter_pub.publish(oBiosig);  
  }
  

  return 0;
}
