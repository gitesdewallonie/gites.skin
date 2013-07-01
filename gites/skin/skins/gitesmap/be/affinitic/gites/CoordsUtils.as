﻿package be.affinitic.gites{		import flash.geom.Point;	public class CoordsUtils 	{				// --		public static const coefficientPixelKilometre:Number= 3.70702693;		public static const rayonTerrestre:Number = 6371;				public function CoordsUtils()		{					}				public static function degToGradiant(deg:Number):Number {			return deg / 180 * Math.PI;		}				public static function calculateDistance(point1:Object,point2:Object):Number {			var lat:Number = degToGradiant(point1.lat);			var long:Number = degToGradiant(point1.long);			var lat2:Number = degToGradiant(point2.lat);			var long2:Number = degToGradiant(point2.long);			var distanceKilometre:Number= Math.acos(Math.sin(lat)*Math.sin(lat2)+Math.cos(lat)*Math.cos(lat2)*Math.cos(long2 - long))*rayonTerrestre;			return distanceKilometre * coefficientPixelKilometre;		}				public static function detectIntersectCircle(centerA:Point , centerB:Point,rayonA:Number,rayonB:Number):Object {			var n1:Number = (Math.pow(rayonB,2)-Math.pow(rayonA,2)-Math.pow(centerB.x,2))+(Math.pow(centerA.x,2)-Math.pow(centerB.y,2)+Math.pow(centerA.y,2));			var n2:Number =(2*(centerA.y-centerB.y));			var n:Number=n1/n2;			var a:Number = Math.pow((centerA.x-centerB.x)/(centerA.y-centerB.y),2)+1;			var b:Number = (2*centerA.y*(centerA.x-centerB.x))/(centerA.y -centerB.y)-(2*n*(centerA.x-centerB.x))/(centerA.y -centerB.y)-2*centerA.x;			var c:Number = Math.pow(centerA.x,2)+Math.pow(centerA.y,2)+Math.pow(n,2)-Math.pow(rayonA,2)-(2*centerA.y*n);			var deltaNumber:Number =Math.sqrt(Math.abs(Math.pow(b,2)-4*a*c));			var x1:Number =(-b+deltaNumber)/(2*a);			var y1:Number = n-x1*((centerA.x-centerB.x)/(centerA.y-centerB.y));			var x2:Number =(-b-deltaNumber)/(2*a);			var y2:Number = n-x2*((centerA.x-centerB.x)/(centerA.y-centerB.y));			var point1= new Point(x1,y1);			var point2= new Point(x2,y2);			return {p1:point1,p2:point2};		}				public static function getGoodPoint(pointToGo:Object,originPoint:Object,o:Object):Point {			var r:Number=calculateDistance(pointToGo,originPoint);			var diff1:Number=Math.pow((o.p1.x-originPoint.xPx),2)+Math.pow((o.p1.y-originPoint.yPx),2)-Math.pow(r,2);			var diff2:Number=Math.pow((o.p2.x-originPoint.xPx),2)+Math.pow((o.p2.y-originPoint.yPx),2)-Math.pow(r,2);			if (Math.abs(diff1)<Math.abs(diff2)) {				return new Point(o.p1.x,o.p1.y);			} else {				return new Point(o.p2.x,o.p2.y);			}		}			}	}