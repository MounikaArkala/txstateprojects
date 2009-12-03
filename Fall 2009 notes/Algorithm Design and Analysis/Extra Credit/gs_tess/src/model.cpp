#include "main.h"
#include "render.h"
#include "model.h"

std::vector<Model*> model;

std::vector<int> modelUpdateList;
int modelUpdateListLock = 0;
DWORD WINAPI ModelUpdateCheckThread(void *lpParameter);


int LoadModel(const char *filename)
{
	if (!filename)
	{
		return LoadModel("default");
	}

	// check if it is already loaded
	for (int n = 0; n < model.size(); n++)
	{
		if (_stricmp(filename, model[n]->name) == 0)
		{
			return n;
		}
	}

	model.push_back(new Model);
	if (model.back()->Load(filename) == -1)
		model.back()->Load("default");

	return model.size() - 1;
}

int Model::Load(const char *filename)
{
	Clear();

	if (!filename)
		return -1;

	char fullname[256];
	sprintf(fullname, "models\\%s.gom", filename);

	FILE *file;
	file = fopen(fullname, "rb");
	if (!file)
		return -1;

	fread(&mesh.radius, sizeof(float), 1, file);
	fread(mesh.min, sizeof(float) * 3, 1, file);
	fread(mesh.max, sizeof(float) * 3, 1, file);
	fread(&mesh.vertices, sizeof(int), 1, file);
	fread(&mesh.indices, sizeof(int), 1, file);
	char texname[128];
	fread(texname, 128, 1, file);
	mesh.tex = CreateTexture(texname, false, false, GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR);
	mesh.vertex = new Vertex [mesh.vertices];
	mesh.index = new unsigned short [mesh.indices];
	fread(mesh.vertex, sizeof(Vertex) * mesh.vertices, 1, file);
	fread(mesh.index, sizeof(unsigned short) * mesh.indices, 1, file);

	fclose(file);

	
	mesh.center[0] = .5f * (mesh.min[0] + mesh.max[0]);
	mesh.center[1] = .5f * (mesh.min[1] + mesh.max[1]);
	mesh.center[2] = .5f * (mesh.min[2] + mesh.max[2]);
	// this is an approximation, but it'll do for now
	mesh.center_radius2 = (mesh.max[0] - mesh.min[0]) * (mesh.max[0] - mesh.min[0])
						+ (mesh.max[1] - mesh.min[1]) * (mesh.max[1] - mesh.min[1])
						+ (mesh.max[2] - mesh.min[2]) * (mesh.max[2] - mesh.min[2]);
	mesh.center_radius = sqrt(mesh.center_radius2);


	glGenBuffersARB(1, &mesh.buffer);
	glBindBufferARB(GL_ARRAY_BUFFER_ARB, mesh.buffer);
	glBufferDataARB(GL_ARRAY_BUFFER_ARB, sizeof(Vertex) * mesh.vertices, mesh.vertex, GL_STATIC_DRAW_ARB);

	glGenBuffersARB(1, &mesh.indexbuffer);
	glBindBufferARB(GL_ELEMENT_ARRAY_BUFFER_ARB, mesh.indexbuffer);
	glBufferDataARB(GL_ELEMENT_ARRAY_BUFFER_ARB, sizeof(unsigned short) * mesh.indices, mesh.index, GL_STATIC_DRAW_ARB);

	strcpy(name, filename);

	return 1;
}

void ModelStartup()
{
	DWORD threadid;
	HANDLE pt = CreateThread(0, 0, ModelUpdateCheckThread, 0, 0, &threadid);
	SetThreadPriority(pt, -1);
	CloseHandle(pt);
}

DWORD WINAPI ModelUpdateCheckThread(void *lpParameter)
{
	HANDLE hDir = CreateFile(
		"models\\",
		GENERIC_READ,
		FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
		NULL,
		OPEN_EXISTING,
		FILE_FLAG_BACKUP_SEMANTICS,
		NULL
	);

	if (hDir == INVALID_HANDLE_VALUE)
		return 0;

	unsigned char *fnbuffer[10000];
	while (1) // could check for a terminate signal...
	{
		FILE_NOTIFY_INFORMATION *fn = (FILE_NOTIFY_INFORMATION *)fnbuffer;
		int bytesreturned = 0;
		if (ReadDirectoryChangesW(hDir, (void *)fnbuffer, 10000, true, FILE_NOTIFY_CHANGE_LAST_WRITE | FILE_NOTIFY_CHANGE_FILE_NAME, (LPDWORD)&bytesreturned, 0, 0))
		{
			while (modelUpdateListLock == 1) // wait until we have access
			{
				Sleep(0);
			}
			modelUpdateListLock = 1;

			while (1)
			{
				if (fn->Action == FILE_ACTION_ADDED || fn->Action == FILE_ACTION_MODIFIED || fn->Action == FILE_ACTION_RENAMED_NEW_NAME)
				{
					char *name;
					name = new char [fn->FileNameLength / 2 + 1];
					wcstombs(name, fn->FileName, fn->FileNameLength / 2 + 1);

					for (int n = 0; n < fn->FileNameLength / 2; n++)
					{
						if (name[n] == '.') // remove extension
						{
							name[n] = 0;
							break;
						}
					}

					for (int n = 0; n < model.size(); n++)
					{
						if (_stricmp(name, model[n]->name) == 0)
						{
							// check for duplicates (seems to create two modified events)
							int i;
							for (i = 0; i < modelUpdateList.size(); i++)
							{
								if (modelUpdateList[i] == n)
									break;
							}
							if (i >= modelUpdateList.size())
								modelUpdateList.push_back(n);
							break;
						}
					}

					delete [] name;
				}

				if (fn->NextEntryOffset == 0)
					break;
				fn = (FILE_NOTIFY_INFORMATION *)(((unsigned char *)fn) + fn->NextEntryOffset);
			}

			modelUpdateListLock = 0;
		}
		else // nothing happened
		{
			Sleep(10);
		}
	}

	CloseHandle(hDir);

	return 1;
}

void UpdateModels()
{
	if (modelUpdateListLock == 1)
		return;

	modelUpdateListLock = 1;
	for (int n = 0; n < modelUpdateList.size(); n++)
	{
		model[modelUpdateList[n]]->Load(model[modelUpdateList[n]]->name);
	}
	modelUpdateList.clear();
	modelUpdateListLock = 0;
}