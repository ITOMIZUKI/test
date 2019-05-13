using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class copytest : MonoBehaviour
{
    public GameObject Cube;
    float time = 3;
    void Update()
    {
        time -= Time.deltaTime;
        if (time <= 0)
        {
            Vector3 CreatePoint = new Vector3(0, 0, 0);
            Instantiate(Cube, CreatePoint, Quaternion.identity);
            time = 3;
        }
    }
}

/*
 using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CreateCube : MonoBehaviour {
    public GameObject Cube;
    float time = 5;
	void Update () {
        time -= Time.deltaTime;
        if(time <= 0)
        {
            Instantiate(Cube);
            time =5;
        }
	}
}
*/