﻿package be.affinitic.gites
{	import flash.display.MovieClip;	public class Chambre extends MovieClip
	{		private var _pk:Number;
		private var _qt:Number;
		private var _minQt:Number;
		private var _title:String;
		private var _localite:String;
		public function Chambre()		{
			highLightMC.visible = false;		}		
		public function set title(sId : String) : void		{			_title = sId;		}		
		public function get title() : String		{			return _title;		}		
		public function set localite(sId : String) : void		{			_localite = sId;		}		
		public function get localite() : String		{			return _localite;		}		
		public function get qt() : Number		{			return _qt;		}		
		public function set qt(nId : Number) : void		{			_qt = nId;		}		
		public function get minQt() : Number		{			return _minQt;		}		
		public function set minQt(nId : Number) : void		{			_minQt = nId;		}		
		public function set pk(nId : Number) : void		{			_pk = nId;		}		
		public function get pk() : Number		{			return _pk;		}	}}