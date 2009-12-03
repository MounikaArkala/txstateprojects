#ifndef INPUT_H
#define INPUT_H

#pragma comment (lib, "dxguid")
#pragma comment (lib, "dinput8")
#define DIRECTINPUT_VERSION 0x0800
#include <dinput.h>
#include <map>
#include <string>

class Input
{
public:

	class Binding
	{
	public:
		std::string name;
		float scale;
		int repeat;
		float repeatstate;
		int joynum;

		Binding(const std::string &_name, const float _scale, const int _repeat, const int _joynum)
		{
			name = _name;
			scale = _scale;
			repeat = _repeat;
			repeatstate = 0;
			joynum = _joynum;
		}

	private:
	};

	LPDIRECTINPUT8			g_DI;
	LPDIRECTINPUTDEVICE8	g_KDIDev;
	LPDIRECTINPUTDEVICE8	g_pMouse;
	std::vector<LPDIRECTINPUTDEVICE8>	g_Joy;

	DIMOUSESTATE2			dims;
	std::vector<DIJOYSTATE>	dijs;
	BYTE					keybuffer[256];

	int Loaded;

	std::map<std::string, int> InputMap; // maps input names to values

	// action, with key/scale pairs
	std::multimap<std::string, Binding> Bindings;

	std::vector<float> deadzone;


	void Startup();
	void Shutdown();

	void Update();
	// add a new input
	void BindInput(std::string keyname, std::string action, float scale, int repeat = 1, int joynum = 0);
	// get an input
	float GetState(std::string action);
	void MapInput();
	void SetDeadzone(int joynum, float value);

	int JoystickCount()
	{
		return g_Joy.size();
	}

private:
	float Input::GetInput(std::multimap<std::string, Binding>::iterator i);
};

extern Input input;

#endif