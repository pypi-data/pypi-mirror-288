from .defines import *

class ResourceManager:
    def __init__(self, helix):
        self.engine = helix
        self.ctx = helix.ctx
        self.shaders = {}
        self.textures = {}

        self.load_texture(
            texture_source=f"{HXASSET_DIR}textures\\tile.png",
            texture_id="default"
        )
        self.load_shader(
            vertex_path=f'{HXASSET_DIR}shaders\\chunk.vert',
            fragment_path=f'{HXASSET_DIR}shaders\\chunk.frag',
            shader_id="chunk"
        )
        self.load_shader(
            vertex_path=f'{HXASSET_DIR}shaders\\marker.vert',
            fragment_path=f'{HXASSET_DIR}shaders\\marker.frag',
            shader_id="marker"
        )

    def set_init_uniforms(self, shader_id) -> None:
        self.shaders[shader_id]["program"]["m_proj"].write(self.engine.camera.m_proj)
        self.shaders[shader_id]["program"]["m_model"].write(glm.mat4())
        try:
            self.shaders[shader_id]["program"]["u_texture_0"] = 0
        except KeyError:
            shader = self.shaders[shader_id]
            hxLogger.log(hxLogger.HLX_LOG_ERROR, msg=f"ResourceManager::ERROR:: `u_texture_0` uniform not present ::{shader["src"]}")

    def load_texture(self, texture_source, texture_id: str):
        texture = pg.image.load(texture_source)
        texture = pg.transform.flip(texture, True, False)

        texture = self.ctx.texture(
            size=texture.get_size(),
            components=4,
            data=pg.image.tostring(texture, 'RGBA', False)
        )
        texture.anisotropy = 32.0
        texture.build_mipmaps()
        texture.filter = (mgl.NEAREST, mgl.NEAREST)
        texture.use(location=0)
        
        self.textures[texture_id] = texture

        return texture

    def get_texture(self, texture_id):
        return self.textures.get(texture_id)

    def load_shader(self, shader_id: str, vertex_path:str, fragment_path:str):
        self.shaders[shader_id] = {}
        self.shaders[shader_id]["src"] = [vertex_path, fragment_path]
        v_path, f_path = self.shaders[shader_id]["src"]

        hxLogger.log(hxLogger.HLX_LOG_SYSTEM, f"Loading shaders: {shader_id}")

        with open(v_path) as vert_file:
            vert_shader = vert_file.read()
            vert_file.close()

        with open(f_path) as frag_file:
            frag_shader = frag_file.read()
            frag_file.close()

        program = self.ctx.program(
            vertex_shader=vert_shader, fragment_shader=frag_shader)
        if not program:
            hxLogger.log(hxLogger.HLX_LOG_ERROR, "Error Compiling/Linking Shaders")
            return None

        program['m_model'].write(glm.mat4())
        self.shaders[shader_id]["program"] = program
        self.set_init_uniforms(shader_id)

        return self.shaders[shader_id]["program"]

    def get_shader(self, shader_id):
        program:mgl.Program = self.shaders[shader_id]["program"]
        hxLogger.log(hxLogger.HLX_LOG_SYSTEM, f"Shader fetched {shader_id}")
        return program
