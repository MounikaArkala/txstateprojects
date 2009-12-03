#include "main.h"
#include "window.h"
#include "input.h"

Input input;

BOOL CALLBACK DIEnumDevicesCallback(LPCDIDEVICEINSTANCE lpddi, LPVOID pvRef)
{
	LPDIRECTINPUTDEVICE8 new_g_Joy;
	DIJOYSTATE new_dijs;

	if (FAILED(input.g_DI->CreateDevice(lpddi->guidInstance, &new_g_Joy, NULL)))
	{
		return DIENUM_CONTINUE;
	}
	new_g_Joy->SetCooperativeLevel(hWnd, DISCL_FOREGROUND | DISCL_NONEXCLUSIVE);
	new_g_Joy->SetDataFormat(&c_dfDIJoystick);
	new_g_Joy->Acquire();

	input.g_Joy.push_back(new_g_Joy);
	input.dijs.push_back(new_dijs);
	input.deadzone.push_back(.1f);

	return DIENUM_CONTINUE;
}

void Input::Startup()
{
	Loaded = 0;

	if (FAILED(DirectInput8Create(GetModuleHandle(NULL), DIRECTINPUT_VERSION, IID_IDirectInput8, (void**)&g_DI, NULL)))
	{
		return;
	}

	if (FAILED(g_DI->CreateDevice(GUID_SysKeyboard, &g_KDIDev, NULL)))
		return;
	g_KDIDev->SetDataFormat(&c_dfDIKeyboard);
	g_KDIDev->SetCooperativeLevel(hWnd, DISCL_FOREGROUND | DISCL_NONEXCLUSIVE);
	g_KDIDev->Acquire();
	DIPROPDWORD  dipdw;
	dipdw.diph.dwSize = sizeof(DIPROPDWORD);
	dipdw.diph.dwHeaderSize = sizeof(DIPROPHEADER);
	dipdw.diph.dwObj = 0;
	dipdw.diph.dwHow = DIPH_DEVICE;
	dipdw.dwData = 10;
	g_KDIDev->SetProperty(DIPROP_BUFFERSIZE, &dipdw.diph);

	if (FAILED(g_DI->CreateDevice(GUID_SysMouse, &g_pMouse, NULL)))
		return;
	g_pMouse->SetDataFormat(&c_dfDIMouse2);
	g_pMouse->SetCooperativeLevel(hWnd, DISCL_FOREGROUND | DISCL_EXCLUSIVE);
	g_pMouse->Acquire();


	g_DI->EnumDevices(DI8DEVCLASS_GAMECTRL, DIEnumDevicesCallback, this, DIEDFL_ATTACHEDONLY);


	MapInput();

	Loaded = 1;

	return;
};

void Input::Shutdown()
{
	Loaded = 0;

	if (g_DI)
    {
        if (g_KDIDev)
        {
            g_KDIDev->Unacquire();
            g_KDIDev->Release();
            g_KDIDev = NULL;
        }
		if (g_pMouse)
		{
			g_pMouse->Unacquire();
			g_pMouse->Release();
			g_pMouse = NULL;
		}

		for (std::vector<LPDIRECTINPUTDEVICE8>::iterator it = g_Joy.begin(); it != g_Joy.end(); ++it)
		{
			(*it)->Unacquire();
			(*it)->Release();
			(*it) = NULL;
		}
		g_Joy.clear();
		dijs.clear();
		deadzone.clear();

        g_DI->Release();
        g_DI = NULL;
    }

	return;
};

void Input::Update()
{
	if (!Loaded)
	{
		return;
	}

	if (GetForegroundWindow() != hWnd)
	{
		memset(&dims, 0, sizeof(DIMOUSESTATE2));
		memset(keybuffer, 0, sizeof(keybuffer));
		for (std::vector<DIJOYSTATE>::iterator it = dijs.begin(); it != dijs.end(); ++it)
		{
			memset(&(*it), 0, sizeof(DIJOYSTATE));
			it->lRx = 32767;
			it->lRy = 32767;
			it->lRz = 32767;
			it->lX = 32767;
			it->lY = 32767;
			it->lZ = 32767;
			it->rgdwPOV[0] = 1;
			it->rgdwPOV[1] = 1;
			it->rgdwPOV[2] = 1;
			it->rgdwPOV[3] = 1;
			it->rglSlider[0] = 32767;
			it->rglSlider[1] = 32767;
		}
		return;
	}

	g_pMouse->Acquire();
	g_pMouse->GetDeviceState(sizeof(DIMOUSESTATE2), &dims);
	g_KDIDev->Acquire();
	g_KDIDev->GetDeviceState(sizeof(keybuffer), &keybuffer);

	for (int n = 0; n < g_Joy.size(); n++)
	{
		g_Joy[n]->Acquire();
		g_Joy[n]->Poll();
		g_Joy[n]->GetDeviceState(sizeof(DIJOYSTATE), &dijs[n]);
	}

	for (std::multimap<std::string, Binding>::iterator i = Bindings.begin(); i != Bindings.end(); ++i)
	{
		if ((*i).second.repeat == 0)
		{
			if ((*i).second.repeatstate == 0)
			{
				(*i).second.repeatstate = GetInput(i);
			}
		}
		else if ((*i).second.repeat == 2)
		{
			if (GetInput(i) == 0)
			{
				(*i).second.repeat = 0;
				(*i).second.repeatstate = 0;
			}
		}
	}
};

float Input::GetInput(std::multimap<std::string, Binding>::iterator i)
{
	float rval = 0;
	float t;
	int inputval = InputMap[(*i).second.name];

	// check to make sure the joystick is connected
	if (inputval >= 400 && inputval < 500)
	{
		if (i->second.joynum >= dijs.size() || i->second.joynum < 0)
		{
			return 0;
		}
	}

	switch (inputval)
	{
	case 300:
	case 301:
	case 302:
	case 303:
	case 304:
	case 305:
	case 306:
	case 307: // mouse buttons
		rval += (dims.rgbButtons[inputval - 300] > 0) * (*i).second.scale;
		break;
	case 308: // mousex
		rval += -dims.lX * (*i).second.scale;
		break;
	case 309: // mousey
		rval += -dims.lY * (*i).second.scale;
		break;
	case 310: // mousez - this has to be handled differently, since return values are weird
		if (dims.lZ > 0)
			rval += 1 * (*i).second.scale;
		else if (dims.lZ < 0)
			rval += -1 * (*i).second.scale;
		break;

	case 400:
	case 401:
	case 402:
	case 403:
	case 404:
	case 405:
	case 406:
	case 407:
	case 408:
	case 409:
	case 410:
	case 411:
	case 412:
	case 413:
	case 414:
	case 415:
	case 416:
	case 417:
	case 418:
	case 419:
	case 420:
	case 421:
	case 422:
	case 423:
	case 424:
	case 425:
	case 426:
	case 427:
	case 428:
	case 429:
	case 430:
	case 431: // joystick buttons
		rval += (dijs[i->second.joynum].rgbButtons[inputval - 400] > 0) * (*i).second.scale;
		break;

	// pov 0
	case 432:
		if (dijs[i->second.joynum].rgdwPOV[0] == 1 || LOWORD(dijs[i->second.joynum].rgdwPOV[0]) == 65535) // centered
			break;
		if (dijs[i->second.joynum].rgdwPOV[0] <= 4500 || dijs[i->second.joynum].rgdwPOV[0] > 31500)
			rval += (*i).second.scale;
		break;
	case 433:
		if (dijs[i->second.joynum].rgdwPOV[0] == 1 || LOWORD(dijs[i->second.joynum].rgdwPOV[0]) == 65535) // centered
			break;
		if (dijs[i->second.joynum].rgdwPOV[0] > 4500 && dijs[i->second.joynum].rgdwPOV[0] <= 13500)
			rval += (*i).second.scale;
		break;
	case 434:
		if (dijs[i->second.joynum].rgdwPOV[0] == 1 || LOWORD(dijs[i->second.joynum].rgdwPOV[0]) == 65535) // centered
			break;
		if (dijs[i->second.joynum].rgdwPOV[0] > 13500 && dijs[i->second.joynum].rgdwPOV[0] <= 22500)
			rval += (*i).second.scale;
		break;
	case 435:
		if (dijs[i->second.joynum].rgdwPOV[0] == 1 || LOWORD(dijs[i->second.joynum].rgdwPOV[0]) == 65535) // centered
			break;
		if (dijs[i->second.joynum].rgdwPOV[0] > 22500 && dijs[i->second.joynum].rgdwPOV[0] <= 31500)
			rval += (*i).second.scale;
		break;

	// pov 1
	case 436:
		if (dijs[i->second.joynum].rgdwPOV[1] == 1 || LOWORD(dijs[i->second.joynum].rgdwPOV[1]) == 65535) // centered
			break;
		if (dijs[i->second.joynum].rgdwPOV[1] <= 4500 || dijs[i->second.joynum].rgdwPOV[1] > 31500)
			rval += (*i).second.scale;
		break;
	case 437:
		if (dijs[i->second.joynum].rgdwPOV[1] == 1 || LOWORD(dijs[i->second.joynum].rgdwPOV[1]) == 65535) // centered
			break;
		if (dijs[i->second.joynum].rgdwPOV[1] > 4500 && dijs[i->second.joynum].rgdwPOV[1] <= 13500)
			rval += (*i).second.scale;
		break;
	case 438:
		if (dijs[i->second.joynum].rgdwPOV[1] == 1 || LOWORD(dijs[i->second.joynum].rgdwPOV[1]) == 65535) // centered
			break;
		if (dijs[i->second.joynum].rgdwPOV[1] > 13500 && dijs[i->second.joynum].rgdwPOV[1] <= 22500)
			rval += (*i).second.scale;
		break;
	case 439:
		if (dijs[i->second.joynum].rgdwPOV[1] == 1 || LOWORD(dijs[i->second.joynum].rgdwPOV[1]) == 65535) // centered
			break;
		if (dijs[i->second.joynum].rgdwPOV[1] > 22500 && dijs[i->second.joynum].rgdwPOV[1] <= 31500)
			rval += (*i).second.scale;
		break;

	// pov 2
	case 440:
		if (dijs[i->second.joynum].rgdwPOV[2] == 1 || LOWORD(dijs[i->second.joynum].rgdwPOV[2]) == 65535) // centered
			break;
		if (dijs[i->second.joynum].rgdwPOV[2] <= 4500 || dijs[i->second.joynum].rgdwPOV[2] > 31500)
			rval += (*i).second.scale;
		break;
	case 441:
		if (dijs[i->second.joynum].rgdwPOV[2] == 1 || LOWORD(dijs[i->second.joynum].rgdwPOV[2]) == 65535) // centered
			break;
		if (dijs[i->second.joynum].rgdwPOV[2] > 4500 && dijs[i->second.joynum].rgdwPOV[2] <= 13500)
			rval += (*i).second.scale;
		break;
	case 442:
		if (dijs[i->second.joynum].rgdwPOV[2] == 1 || LOWORD(dijs[i->second.joynum].rgdwPOV[2]) == 65535) // centered
			break;
		if (dijs[i->second.joynum].rgdwPOV[2] > 13500 && dijs[i->second.joynum].rgdwPOV[2] <= 22500)
			rval += (*i).second.scale;
		break;
	case 443:
		if (dijs[i->second.joynum].rgdwPOV[2] == 1 || LOWORD(dijs[i->second.joynum].rgdwPOV[2]) == 65535) // centered
			break;
		if (dijs[i->second.joynum].rgdwPOV[2] > 22500 && dijs[i->second.joynum].rgdwPOV[2] <= 31500)
			rval += (*i).second.scale;
		break;

	// pov 3
	case 444:
		if (dijs[i->second.joynum].rgdwPOV[3] == 1 || LOWORD(dijs[i->second.joynum].rgdwPOV[3]) == 65535) // centered
			break;
		if (dijs[i->second.joynum].rgdwPOV[3] <= 4500 || dijs[i->second.joynum].rgdwPOV[3] > 31500)
			rval += (*i).second.scale;
		break;
	case 445:
		if (dijs[i->second.joynum].rgdwPOV[3] == 1 || LOWORD(dijs[i->second.joynum].rgdwPOV[3]) == 65535) // centered
			break;
		if (dijs[i->second.joynum].rgdwPOV[3] > 4500 && dijs[i->second.joynum].rgdwPOV[3] <= 13500)
			rval += (*i).second.scale;
		break;
	case 446:
		if (dijs[i->second.joynum].rgdwPOV[3] == 1 || LOWORD(dijs[i->second.joynum].rgdwPOV[3]) == 65535) // centered
			break;
		if (dijs[i->second.joynum].rgdwPOV[3] > 13500 && dijs[i->second.joynum].rgdwPOV[3] <= 22500)
			rval += (*i).second.scale;
		break;
	case 447:
		if (dijs[i->second.joynum].rgdwPOV[3] == 1 || LOWORD(dijs[i->second.joynum].rgdwPOV[3]) == 65535) // centered
			break;
		if (dijs[i->second.joynum].rgdwPOV[3] > 22500 && dijs[i->second.joynum].rgdwPOV[3] <= 31500)
			rval += (*i).second.scale;
		break;

	case 448:
	case 449: // sliders
		break;

	case 450: // axes
		t = 1.0f - dijs[i->second.joynum].lX / 32767.0f;
		if (fabs(t) < deadzone[i->second.joynum])
			t = 0;
		// scale input so it is in 0-1 range after deadzone
		if (t < 0)
			rval += (t + deadzone[i->second.joynum]) * (1.0f / (1.0f - deadzone[i->second.joynum])) * (*i).second.scale;
		else if (t > 0)
			rval += (t - deadzone[i->second.joynum]) * (1.0f / (1.0f - deadzone[i->second.joynum])) * (*i).second.scale;
		else // no input
			rval = 0;
		break;
	case 451:
		t = 1.0f - dijs[i->second.joynum].lY / 32767.0f;
		if (fabs(t) < deadzone[i->second.joynum])
			t = 0;
		// scale input so it is in 0-1 range after deadzone
		if (t < 0)
			rval += (t + deadzone[i->second.joynum]) * (1.0f / (1.0f - deadzone[i->second.joynum])) * (*i).second.scale;
		else if (t > 0)
			rval += (t - deadzone[i->second.joynum]) * (1.0f / (1.0f - deadzone[i->second.joynum])) * (*i).second.scale;
		else // no input
			rval = 0;
		break;
	case 452:
		t = 1.0f - dijs[i->second.joynum].lZ / 32767.0f;
		if (fabs(t) < deadzone[i->second.joynum])
			t = 0;
		// scale input so it is in 0-1 range after deadzone
		if (t < 0)
			rval += (t + deadzone[i->second.joynum]) * (1.0f / (1.0f - deadzone[i->second.joynum])) * (*i).second.scale;
		else if (t > 0)
			rval += (t - deadzone[i->second.joynum]) * (1.0f / (1.0f - deadzone[i->second.joynum])) * (*i).second.scale;
		else // no input
			rval = 0;
		break;
	case 453: // rotation axes
		t = 1.0f - dijs[i->second.joynum].lRx / 32767.0f;
		if (fabs(t) < deadzone[i->second.joynum])
			t = 0;
		// scale input so it is in 0-1 range after deadzone
		if (t < 0)
			rval += (t + deadzone[i->second.joynum]) * (1.0f / (1.0f - deadzone[i->second.joynum])) * (*i).second.scale;
		else if (t > 0)
			rval += (t - deadzone[i->second.joynum]) * (1.0f / (1.0f - deadzone[i->second.joynum])) * (*i).second.scale;
		else // no input
			rval = 0;
		break;
	case 454:
		t = 1.0f - dijs[i->second.joynum].lRy / 32767.0f;
		if (fabs(t) < deadzone[i->second.joynum])
			t = 0;
		// scale input so it is in 0-1 range after deadzone
		if (t < 0)
			rval += (t + deadzone[i->second.joynum]) * (1.0f / (1.0f - deadzone[i->second.joynum])) * (*i).second.scale;
		else if (t > 0)
			rval += (t - deadzone[i->second.joynum]) * (1.0f / (1.0f - deadzone[i->second.joynum])) * (*i).second.scale;
		else // no input
			rval = 0;
		break;
	case 455:
		t = 1.0f - dijs[i->second.joynum].lRz / 32767.0f;
		if (fabs(t) < deadzone[i->second.joynum])
			t = 0;
		// scale input so it is in 0-1 range after deadzone
		if (t < 0)
			rval += (t + deadzone[i->second.joynum]) * (1.0f / (1.0f - deadzone[i->second.joynum])) * (*i).second.scale;
		else if (t > 0)
			rval += (t - deadzone[i->second.joynum]) * (1.0f / (1.0f - deadzone[i->second.joynum])) * (*i).second.scale;
		else // no input
			rval = 0;
		break;

	default: // keyboard
		if (inputval < 1 || inputval > 221)
			break;
		if (keybuffer[inputval] & 0x80)
		{
			rval += (*i).second.scale;
		}
		break;
	};

	return rval;
}

float Input::GetState(std::string action)
{
	std::pair<std::multimap<std::string, Binding>::iterator, std::multimap<std::string, Binding>::iterator> bounds;
	bounds = Bindings.equal_range(action);

	float rval = 0;
	for (std::multimap<std::string, Binding>::iterator i = bounds.first; i != bounds.second; ++i)
	{
		if ((*i).second.repeat == 0 && (*i).second.repeatstate != 0)
		{
			rval += (*i).second.repeatstate;
			(*i).second.repeat = 2;
			continue;
		}
		else if ((*i).second.repeat == 2)
		{
			continue;
		}

		rval += GetInput(i);
	}

	return rval;
}

void Input::BindInput(std::string keyname, std::string action, float scale, int repeat, int joynum)
{
	Bindings.insert(std::pair<std::string, Binding>(action, Binding(keyname, scale, repeat, joynum)));
}

void Input::MapInput()
{
	InputMap["escape"]	= 1;
	InputMap["1"]	= 2;
	InputMap["2"]	= 3;
	InputMap["3"]	= 4;
	InputMap["4"]	= 5;
	InputMap["5"]	= 6;
	InputMap["6"]	= 7;
	InputMap["7"]	= 8;
	InputMap["8"]	= 9;
	InputMap["9"]	= 10;
	InputMap["0"]	= 11;
	InputMap["minus"]	= 12;
	InputMap["equals"]	= 13;
	InputMap["back"]	= 14;
	InputMap["tab"]	= 15;
	InputMap["q"]	= 16;
	InputMap["w"]	= 17;
	InputMap["e"]	= 18;
	InputMap["r"]	= 19;
	InputMap["t"]	= 20;
	InputMap["y"]	= 21;
	InputMap["u"]	= 22;
	InputMap["i"]	= 23;
	InputMap["o"]	= 24;
	InputMap["p"]	= 25;
	InputMap["lbracket"]	= 26;
	InputMap["rbracket"]	= 27;
	InputMap["return"]	= 28;
	InputMap["lcontrol"]	= 29;
	InputMap["a"]	= 30;
	InputMap["s"]	= 31;
	InputMap["d"]	= 32;
	InputMap["f"]	= 33;
	InputMap["g"]	= 34;
	InputMap["h"]	= 35;
	InputMap["j"]	= 36;
	InputMap["k"]	= 37;
	InputMap["l"]	= 38;
	InputMap["semicolon"]	= 39;
	InputMap["apostrophe"]	= 40;
	InputMap["grave"]	= 41;
	InputMap["lshift"]	= 42;
	InputMap["backslash"]	= 43;
	InputMap["z"]	= 44;
	InputMap["x"]	= 45;
	InputMap["c"]	= 46;
	InputMap["v"]	= 47;
	InputMap["b"]	= 48;
	InputMap["n"]	= 49;
	InputMap["m"]	= 50;
	InputMap["comma"]	= 51;
	InputMap["period"]	= 52;
	InputMap["slash"]	= 53;
	InputMap["rshift"]	= 54;
	InputMap["multiply"]	= 55;
	InputMap["lalt"]	= 56;
	InputMap["space"]	= 57;
	InputMap["capital"]	= 58;
	InputMap["f1"]	= 59;
	InputMap["f2"]	= 60;
	InputMap["f3"]	= 61;
	InputMap["f4"]	= 62;
	InputMap["f5"]	= 63;
	InputMap["f6"]	= 64;
	InputMap["f7"]	= 65;
	InputMap["f8"]	= 66;
	InputMap["f9"]	= 67;
	InputMap["f10"]	= 68;
	InputMap["numlock"]	= 69;
	InputMap["scroll"]	= 70;
	InputMap["numpad7"]	= 71;
	InputMap["numpad8"]	= 72;
	InputMap["numpad9"]	= 73;
	InputMap["subtract"]	= 74;
	InputMap["numpad4"]	= 75;
	InputMap["numpad5"]	= 76;
	InputMap["numpad6"]	= 77;
	InputMap["add"]	= 78;
	InputMap["numpad1"]	= 79;
	InputMap["numpad2"]	= 80;
	InputMap["numpad3"]	= 81;
	InputMap["numpad0"]	= 82;
	InputMap["decimal"]	= 83;
	InputMap["f11"]	= 87;
	InputMap["f12"]	= 88;
	InputMap["numpadenter"]	= 156;
	InputMap["rcontrol"]	= 157;
	InputMap["divide"]	= 181;
	InputMap["sysrq"]	= 183;
	InputMap["ralt"]	= 184;
	InputMap["pause"]	= 197;
	InputMap["home"]	= 199;
	InputMap["up"]	= 200;
	InputMap["pgup"]	= 201;
	InputMap["left"]	= 203;
	InputMap["right"]	= 205;
	InputMap["end"]	= 207;
	InputMap["down"]	= 208;
	InputMap["pgdn"]	= 209;
	InputMap["insert"]	= 210;
	InputMap["delete"]	= 211;
	InputMap["lwin"]	= 219;
	InputMap["rwin"]	= 220;
	InputMap["apps"]	= 221;

	// mouse input
	InputMap["mouse0"] = 300;
	InputMap["mouse1"] = 301;
	InputMap["mouse2"] = 302;
	InputMap["mouse3"] = 303;
	InputMap["mouse4"] = 304;
	InputMap["mouse5"] = 305;
	InputMap["mouse6"] = 306;
	InputMap["mouse7"] = 307;
	InputMap["mousex"] = 308;
	InputMap["mousey"] = 309;
	InputMap["mousez"] = 310;

	// joystick input
	InputMap["joy0"] = 400;
	InputMap["joy1"] = 401;
	InputMap["joy2"] = 402;
	InputMap["joy3"] = 403;
	InputMap["joy4"] = 404;
	InputMap["joy5"] = 405;
	InputMap["joy6"] = 406;
	InputMap["joy7"] = 407;
	InputMap["joy8"] = 408;
	InputMap["joy9"] = 409;
	InputMap["joy10"] = 410;
	InputMap["joy11"] = 411;
	InputMap["joy12"] = 412;
	InputMap["joy13"] = 413;
	InputMap["joy14"] = 414;
	InputMap["joy15"] = 415;
	InputMap["joy16"] = 416;
	InputMap["joy17"] = 417;
	InputMap["joy18"] = 418;
	InputMap["joy19"] = 419;
	InputMap["joy20"] = 420;
	InputMap["joy21"] = 421;
	InputMap["joy22"] = 422;
	InputMap["joy23"] = 423;
	InputMap["joy24"] = 424;
	InputMap["joy25"] = 425;
	InputMap["joy26"] = 426;
	InputMap["joy27"] = 427;
	InputMap["joy28"] = 428;
	InputMap["joy29"] = 429;
	InputMap["joy30"] = 430;
	InputMap["joy31"] = 431;

	InputMap["joypov0n"] = 432;
	InputMap["joypov0e"] = 433;
	InputMap["joypov0s"] = 434;
	InputMap["joypov0w"] = 435;

	InputMap["joypov1n"] = 436;
	InputMap["joypov1e"] = 437;
	InputMap["joypov1s"] = 438;
	InputMap["joypov1w"] = 439;

	InputMap["joypov2n"] = 440;
	InputMap["joypov2e"] = 441;
	InputMap["joypov2s"] = 442;
	InputMap["joypov2w"] = 443;

	InputMap["joypov3n"] = 444;
	InputMap["joypov3e"] = 445;
	InputMap["joypov3s"] = 446;
	InputMap["joypov3w"] = 447;

	InputMap["joyslider0"] = 448;
	InputMap["joyslider1"] = 449;

	InputMap["joyx"] = 450;
	InputMap["joyy"] = 451;
	InputMap["joyz"] = 452;
	InputMap["joyrx"] = 453;
	InputMap["joyry"] = 454;
	InputMap["joyrz"] = 455;
}

void Input::SetDeadzone(int joynum, float value)
{
	if (joynum >= deadzone.size() || joynum < 0 || value < 0 || value > 1)
		return;

	deadzone[joynum] = value;
}