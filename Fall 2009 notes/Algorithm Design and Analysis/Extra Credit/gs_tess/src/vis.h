#ifndef VIS_H
#define VIS_H

struct Plane
{
	float n[3];
	float d;
};

class CleaveData
{
public:
	std::vector<Plane> plane;

	int adjoinsc;


	// returns -1 if the point is inside all planes, otherwise the first plane it is outside
	int IsOutside(const float *point)
	{
		for (int n = 0; n < plane.size(); n++)
		{
			float d2 = plane[n].n[0] * point[0] + plane[n].n[1] * point[1] + plane[n].n[2] * point[2];
			if (d2 < plane[n].d - .00001f)
				return n;
		}
		return -1;
	}

	int IsOutside2(const float *point, const float radius)
	{
		for (int n = 0; n < plane.size(); n++)
		{
			float d2 = plane[n].n[0] * point[0] + plane[n].n[1] * point[1] + plane[n].n[2] * point[2];
			if (d2 < plane[n].d - radius)
				return n;
		}
		return -1;
	}

	void AddPlane(const Plane &p)
	{
		plane.push_back(p);
	}
	void DeletePlane(int p)
	{
		//plane.erase(&plane[p]);
		plane.erase(plane.begin() + p);
	}

	CleaveData()
	{
		adjoinsc = -1;
	}
};

void Vis();

#endif