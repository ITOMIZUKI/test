using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;
using System.Text;
//using System.Threading.Tasks;
using System.IO;



public class csvextractor : MonoBehaviour {

	// Use this for initialization
	void Start () {
        StreamReader sr = new StreamReader(
            @"C: \Users\turara\Desktop\段ボール\HOSHITO\position");
        {
            // read a line from csv file
            string line = sr.ReadLine();
            // separate line by canma and put them into array
            string[] values = line.Split(',');

            //put string list factors into general list
            List<string> lists = new List<string>();
            lists.AddRange(values);

            //print console
            foreach (string list in lists)
            {
                System.Console.Write("{0}", list);
            }
            System.Console.WriteLine();
        }
	}
	
	// Update is called once per frame
	void Update () {
		
	}
}
