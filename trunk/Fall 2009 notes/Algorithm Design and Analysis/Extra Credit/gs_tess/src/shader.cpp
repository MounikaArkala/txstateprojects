#include "main.h"
#include "render.h"

enum ShaderType
{
	SHADER_VERTEX,
	SHADER_GEOMETRY,
	SHADER_FRAGMENT,
};

// program fragments
struct ShaderInfo
{
	unsigned int id;
	char name[MAX_SHADER_NAME];
	ShaderType type;
	std::set<int> dependent_programs;
};
std::vector<ShaderInfo> shader;

// linked programs
std::vector<ProgramInfo> program;


std::vector<int> shaderupdatelist;
int shaderupdatelistlock = 0;
DWORD WINAPI ShaderUpdateCheckThread(void *lpParameter);

const int shader_buffer_len = 10000;
const int info_log_buffer_len = 10000;
char shader_source[shader_buffer_len];
char info_log[info_log_buffer_len];

bool UpdateShader(int shader_num, std::set<int> &relink_programs)
{
	FILE *shaderlog = fopen("shaderlog.txt", "a+");

	char fullname[256];
	switch (shader[shader_num].type)
	{
	case SHADER_VERTEX:
		sprintf(fullname, "shaders\\%s.shv", shader[shader_num].name);
		break;
	case SHADER_GEOMETRY:
		sprintf(fullname, "shaders\\%s.shg", shader[shader_num].name);
		break;
	case SHADER_FRAGMENT:
		sprintf(fullname, "shaders\\%s.shf", shader[shader_num].name);
		break;
	default:
		fprintf(shaderlog, "Updating Shader Failed: Unknown shader type\n");
		fclose(shaderlog);
		return false;
	}

	fprintf(shaderlog, "\n\nUpdating Shader:	%s\n", fullname);


	FILE *file;
	int shaderlen;
	int rval;

	file = fopen(fullname, "rb");
	if (!file)
	{
		fprintf(shaderlog, "	Failed to load file: %s\n", fullname);
		return false;
	}
	shaderlen = _filelength(file->_file);
	fread(shader_source, shaderlen, 1, file);
	fclose(file);

	// need a pointer to an actual pointer
	char *spp = (char *)&shader_source;
	// source, compile, and check for errors
	glShaderSource(shader[shader_num].id, 1, (const GLchar**)&spp, &shaderlen);
	glCompileShader(shader[shader_num].id);
	glGetShaderiv(shader[shader_num].id, GL_COMPILE_STATUS, &rval);
	if (rval)
		fprintf(shaderlog, "	Shader %s compile: success\n", fullname);
	else
		fprintf(shaderlog, "	Shader %s compile: fail\n", fullname);
	glGetShaderInfoLog(shader[shader_num].id, info_log_buffer_len, &rval, info_log);
	fprintf(shaderlog, "	Info Log:\n%s\n\n", info_log);


	fclose(shaderlog);


	relink_programs.insert(shader[shader_num].dependent_programs.begin(), shader[shader_num].dependent_programs.end());


	return true;
}

int AppendShaderIncludes(const char *filename, ShaderType type, FILE *shaderlog, std::set<std::string> &shader_includes)
{
	int count = 0;

	char fullname[256];
	switch (type)
	{
	case SHADER_VERTEX:
		sprintf(fullname, "shaders\\%s.shv", filename);
		break;
	case SHADER_GEOMETRY:
		sprintf(fullname, "shaders\\%s.shg", filename);
		break;
	case SHADER_FRAGMENT:
		sprintf(fullname, "shaders\\%s.shf", filename);
		break;
	default:
		return count;
		break;
	}

	const int buffer_size = 1024;
	char buffer[1024];

	FILE *file = fopen(fullname, "rt");
	if (!fgets(buffer, buffer_size, file))
	{
		// nothing to read
		fclose(file);
		return count;
	}
	fclose(file);

	if (strnicmp(buffer, "//link:", strlen("//link:")) == 0)
	{
		char *p = buffer;
		p += strlen("//link:");

		char include_name[MAX_SHADER_NAME];

		int bytes_read;
		while (1 == sscanf(p, " %s%n", include_name, &bytes_read))
		{
			if (shader_includes.insert(include_name).second) // insert
			{
				fprintf(shaderlog, "	link %s...\n", include_name);
				count++; // and increment our count if it's not a duplicate
			}
			p += bytes_read;
		}
	}

	return count;
}

bool LoadShader(const char *filename, ShaderType type, FILE *shaderlog, std::set<int> &shaderlist)
{
	std::set<std::string> shaders_needed;
	// we need at least this one
	shaders_needed.insert(filename);
	// we could support multiple levels of linking, but it's already a pain having to prototype everything in the shader
	// links are not updates on shader updates
	AppendShaderIncludes(filename, type, shaderlog, shaders_needed);


	for (std::set<std::string>::iterator it = shaders_needed.begin(); it != shaders_needed.end(); ++it)
	{
		// has it already been loaded?
		for (int n = 0; n < shader.size(); n++)
		{
			if (_strnicmp(it->c_str(), shader[n].name, MAX_SHADER_NAME) == 0
				&& type == shader[n].type)
			{
				// add this to the list of shaders to be linked
				shaderlist.insert(n);
			}
		}

		char fullname[256];
		unsigned int shaderid;
		switch (type)
		{
		case SHADER_VERTEX:
			sprintf(fullname, "shaders\\%s.shv", it->c_str());
			shaderid = glCreateShader(GL_VERTEX_SHADER);
			break;
		case SHADER_GEOMETRY:
			sprintf(fullname, "shaders\\%s.shg", it->c_str());
			shaderid = glCreateShader(GL_GEOMETRY_SHADER_EXT);
			break;
		case SHADER_FRAGMENT:
			sprintf(fullname, "shaders\\%s.shf", it->c_str());
			shaderid = glCreateShader(GL_FRAGMENT_SHADER);
			break;
		default:
			fprintf(shaderlog, "	Unknown shader type\n");
			return false;
		}


		FILE *file;
		int shaderlen;
		int rval;

		file = fopen(fullname, "rb");
		if (!file)
		{
			fprintf(shaderlog, "	Failed to load file: %s\n", fullname);
			return false;
		}
		shaderlen = _filelength(file->_file);
		fread(shader_source, shaderlen, 1, file);
		fclose(file);

		// need a pointer to an actual pointer
		char *spp = (char *)&shader_source;
		// source, compile, and check for errors
		glShaderSource(shaderid, 1, (const GLchar**)&spp, &shaderlen);
		glCompileShader(shaderid);
		glGetShaderiv(shaderid, GL_COMPILE_STATUS, &rval);
		if (rval)
			fprintf(shaderlog, "	Shader %s compile: success\n", fullname);
		else
			fprintf(shaderlog, "	Shader %s compile: fail\n", fullname);
		glGetShaderInfoLog(shaderid, info_log_buffer_len, &rval, info_log);
		fprintf(shaderlog, "	Info Log:\n%s\n", info_log);



		ShaderInfo newshader;

		newshader.id = shaderid;
		newshader.type = type;
		strcpy(newshader.name, it->c_str());

		shader.push_back(newshader);

		// add this to the list of shaders to be linked
		shaderlist.insert(shader.size() - 1);
	}

	return true;
}

void RelinkProgram(int program_num)
{
	FILE *shaderlog = fopen("shaderlog.txt", "a+");
	fprintf(shaderlog, "Relinking Program:	%s.shv	%s.shf\n", program[program_num].vshader, program[program_num].fshader);

	int rval;

	glLinkProgram(program[program_num].id);
	glGetProgramiv(program[program_num].id, GL_LINK_STATUS, &rval);
	// need to include the attached shader names
	if (rval)
		fprintf(shaderlog, "	Program link: success\n");
	else
		fprintf(shaderlog, "	Program link: fail\n");
	glGetProgramInfoLog(program[program_num].id, info_log_buffer_len, &rval, info_log);
	fprintf(shaderlog, "	Info Log:\n%s\n\n", info_log);

	fclose(shaderlog);
}

int CreateProgram(const char *vshader, const char *gshader, const char *fshader, GLenum gs_in/* = GL_TRIANGLES*/, GLenum gs_out/* = GL_TRIANGLE_STRIP*/, GLenum gs_outmax/* = 3*/)
{
	bool geom_shader_enabled = strlen(gshader) > 0;

	for (int n = 0; n < program.size(); n++)
	{
		if (_strnicmp(vshader, program[n].vshader, MAX_SHADER_NAME) == 0
			&& _strnicmp(gshader, program[n].gshader, MAX_SHADER_NAME) == 0
			&& _strnicmp(fshader, program[n].fshader, MAX_SHADER_NAME) == 0)
		{
			return n;
		}
	}

	FILE *shaderlog = fopen("shaderlog.txt", "a+");
	fprintf(shaderlog, "\n\nCreating Program:	%s.shv	%s.shf\n", vshader, fshader);


	// get all shaders required...
	std::set<int> shaderlist;
	fprintf(shaderlog, "	Vertex:\n");
	if (!LoadShader(vshader, SHADER_VERTEX, shaderlog, shaderlist))
	{
		fprintf(shaderlog, "	Unable to load all required shaders\n");
		return -1;
	}
	// we would want to allow passing a null pointer for the geometry shader to disable it
	if (geom_shader_enabled)
	{
		fprintf(shaderlog, "	Geometry:\n");
		if (!LoadShader(gshader, SHADER_GEOMETRY, shaderlog, shaderlist))
		{
			fprintf(shaderlog, "	Unable to load all required shaders\n");
			return -1;
		}
	}
	fprintf(shaderlog, "	Fragment:\n");
	if (!LoadShader(fshader, SHADER_FRAGMENT, shaderlog, shaderlist))
	{
		fprintf(shaderlog, "	Unable to load all required shaders\n");
		return -1;
	}


	// link program
	int rval;
	unsigned int programid = glCreateProgram();

	if (geom_shader_enabled)
	{
		glProgramParameteriEXT(programid, GL_GEOMETRY_INPUT_TYPE_EXT, gs_in);
		glProgramParameteriEXT(programid, GL_GEOMETRY_OUTPUT_TYPE_EXT, gs_out);

		// max output can also be determined by max output components / output components per vertex - seems more likely
		int geom_output_max_vertices = 0;
		glGetIntegerv(GL_MAX_GEOMETRY_OUTPUT_VERTICES_EXT, &geom_output_max_vertices);
		fprintf(shaderlog, "	Geometry shader max output vertices: %d\n", geom_output_max_vertices);

		glProgramParameteriEXT(programid, GL_GEOMETRY_VERTICES_OUT_EXT, gs_outmax);
	}

	// attached shaders do not need to be compiled or even supplied a source string at this point
	for (std::set<int>::iterator it = shaderlist.begin(); it != shaderlist.end(); ++it)
	{
		glAttachShader(programid, shader[*it].id);
	}

	// attached shaders must be compiled
	// subsequent modifications and recompiling of shaders will not affect the linked program
	// if the currently active program is relinked, it will remain active using the newly linked code
	// relinking a program resets uniform values
	glLinkProgram(programid);
	glGetProgramiv(programid, GL_LINK_STATUS, &rval);
	// need to include the attached shader names
	if (rval)
		fprintf(shaderlog, "	Program link: success\n");
	else
		fprintf(shaderlog, "	Program link: fail\n");
	glGetProgramInfoLog(programid, info_log_buffer_len, &rval, info_log);
	fprintf(shaderlog, "	Info Log:\n%s\n\n", info_log);

	fclose(shaderlog);


	// add it to the list of programs
	ProgramInfo newprogram;

	newprogram.id = programid;
	strcpy(newprogram.vshader, vshader);
	strcpy(newprogram.gshader, gshader);
	strcpy(newprogram.fshader, fshader);

	program.push_back(newprogram);

	int program_num = program.size() - 1;

	// update dependencies!
	for (std::set<int>::iterator it = shaderlist.begin(); it != shaderlist.end(); ++it)
	{
		shader[*it].dependent_programs.insert(program_num);
	}

	return program_num;
}

void ShaderStartup()
{
	// remove the old shader log - don't need this if we do an initial non-appending output (program limits?)
	DeleteFile("shaderlog.txt");

	// update thread
	DWORD threadid;
	HANDLE pt = CreateThread(0, 0, ShaderUpdateCheckThread, 0, 0, &threadid);
	SetThreadPriority(pt, -1);
	CloseHandle(pt);
}

void ShaderShutdown()
{
}

DWORD WINAPI ShaderUpdateCheckThread(void *lpParameter)
{
	HANDLE hDir = CreateFile(
		"shaders\\",
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
			while (shaderupdatelistlock == 1) // wait until we have access
			{
				Sleep(0);
			}
			shaderupdatelistlock = 1;

			while (1)
			{
				if (fn->Action == FILE_ACTION_ADDED || fn->Action == FILE_ACTION_MODIFIED || fn->Action == FILE_ACTION_RENAMED_NEW_NAME)
				{
					char *name;
					name = new char [fn->FileNameLength / 2 + 1];
					wcstombs(name, fn->FileName, fn->FileNameLength / 2 + 1);

					ShaderType type;

					for (int n = 0; n < fn->FileNameLength / 2; n++)
					{
						if (name[n] == '.') // remove extension
						{
							name[n] = 0;

							// get the type by file extension
							if (n + 3 < fn->FileNameLength / 2)
							{
								if (name[n + 3] == 'v')
									type = SHADER_VERTEX;
								else if (name[n + 3] == 'g')
									type = SHADER_GEOMETRY;
								else
									type = SHADER_FRAGMENT;
							}
							break;
						}
					}

					for (int n = 0; n < shader.size(); n++)
					{
						if (_stricmp(name, shader[n].name) == 0 && type == shader[n].type)
						{
							// check for duplicates (seems to create two modified events
							int i;
							for (i = 0; i < shaderupdatelist.size(); i++)
							{
								if (shaderupdatelist[i] == n)
									break;
							}
							if (i >= shaderupdatelist.size())
								shaderupdatelist.push_back(n);
							break;
						}
					}

					delete [] name;
				}

				if (fn->NextEntryOffset == 0)
					break;
				fn = (FILE_NOTIFY_INFORMATION *)(((unsigned char *)fn) + fn->NextEntryOffset);
			}

			shaderupdatelistlock = 0;
		}
		else // nothing happened
		{
			Sleep(10);
		}
	}

	CloseHandle(hDir);

	return 1;
}

void UpdateShaders()
{
	if (shaderupdatelistlock == 1)
		return;
	shaderupdatelistlock = 1;

	// update shaders and get a list of all dependent programs that must be relinked
	std::set<int> relink_programs;
	for (int n = 0; n < shaderupdatelist.size(); n++)
	{
		UpdateShader(shaderupdatelist[n], relink_programs);
	}
	shaderupdatelist.clear();

	for (std::set<int>::iterator it = relink_programs.begin(); it != relink_programs.end(); ++it)
	{
		RelinkProgram(*it);
	}

	shaderupdatelistlock = 0;
}