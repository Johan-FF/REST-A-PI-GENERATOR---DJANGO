from .script_method.windows_script import WindowsCreator
from .script_method.linux_script import LinuxCreator
from .builder import Builder
from script_builder.concrete_script import ConcreteScript

class NestApiBuilder(Builder):
    """
    The Concrete Builder classes follow the Builder interface and provide
    specific implementations of the building steps. Your program may have
    several variations of Builders, implemented differently.
    """

    PROJECT_NAME: str = ""
    VERSION: str = ""
    EXECUTE_PORT: str = ""
    OPERATING_SYSTEM: str = ""

    def __init__(self, psm_model) -> None:
        """
        A fresh builder instance should contain a blank script object, which is
        used in further assembly.
        """
        NestApiBuilder.OPERATING_SYSTEM = psm_model.find("so").get("so-name")

        project_name = psm_model.find("project").get("name")
        NestApiBuilder.PROJECT_NAME = project_name

        technology = psm_model.find("technology")
        NestApiBuilder.EXECUTE_PORT = technology.get("port")
        NestApiBuilder.VERSION = technology.get("version")

        self.reset()
        
    def reset(self) -> None:
        self._script = ConcreteScript()

        if NestApiBuilder.OPERATING_SYSTEM=="WINDOWS":
            self.script_method = WindowsCreator()
        else:
            self.script_method = LinuxCreator()
        self.script_method.add_comment("Nombre del proyecto")
        self.script_method.add_enter_project_packague(NestApiBuilder.PROJECT_NAME)
        self.script_method.add_powerShellCommand("Start-Process cmd -ArgumentList '/c nest new %PROJECT_NAME%','--package-manager npm' -NoNewWindow -Wait")
        self.script_method.add_comment("Entrando src...")
        self.script_method.add_cd("tienda\src")

    @property
    def script(self) -> ConcreteScript:
        """
        Concrete Builders are supposed to provide their own methods for
        retrieving results. That's because various types of builders may create
        entirely different scripts that don't follow the same interface.
        Therefore, such methods cannot be declared in the base Builder interface
        (at least in a statically typed programming language).

        Usually, after returning the end result to the client, a builder
        instance is expected to be ready to start producing another script.
        That's why it's a usual practice to call the reset method at the end of
        the `getScript` method body. However, this behavior is not mandatory,
        and you can make your builders wait for an explicit reset call from the
        client code before disposing of the previous result.
        """
        script = self.script_method._script
        self.reset()
        return script
    
    def produce_create(self):
        pass

    def produce_crud(self, entity_name, attributes: list[dict], relations, dependencies):
        self.script_method.add_comment(f"Creando modulo {entity_name.lower()}...")
        self.script_method.add_print(f"Creando modulo {entity_name.lower()}...")
        self.script_method.add_powerShellCommand(f"Start-Process cmd -ArgumentList '/c nest generate resource {entity_name.lower()} ' -NoNewWindow -Wait")
        self.script_method.add_cd(entity_name.lower())
        self.script_method.add_cd("entities")
        #Create entity
        codeEntity = self.produce_entity(entity_name, attributes, relations, dependencies)
        self.script_method.add_command(codeEntity)
        self.script_method.add_cd("..")
        self.script_method.add_cd("..")
        #Create dto
        self.script_method.add_cd(entity_name.lower())
        self.script_method.add_cd("dto")
        codeDto = self.produce_dto(entity_name, attributes, relations, dependencies)
        self.script_method.add_command(codeDto)
        self.script_method.add_cd("..")
        self.script_method.add_cd("..")
        #Create service
        self.script_method.add_cd(entity_name.lower())
        codeService = self.produce_service(entity_name, attributes, relations, dependencies)
        self.script_method.add_command(codeService)
        self.script_method.add_cd("..")
        self.script_method.add_cd("..")
        #Config modules
        self.script_method.add_cd(entity_name.lower())
        codeModule = self.config_Module( entity_name, attributes, relations, dependencies)
        self.script_method.add_command(codeModule)
        #Create Controller
        codeController = self.produce_controller( entity_name, attributes, relations, dependencies)
        self.script_method.add_command(codeController)
        self.script_method.add_cd("..")
        self.script_method.add_cd("..")
        
    
    def produce_controller(self, entity_name, attributes):
        codeController = '@echo off\npowershell -Command ^\n'
        codeController += f"    \"Set-Content -Path '{entity_name.lower()}.controller.ts' -Value $null;\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" 'import { Controller, Get, Post, Body, Patch, Param, Delete, Put, UsePipes, ValidationPipe, ParseIntPipe } from ''@nestjs/common'';';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" 'import { ApiBody, ApiOperation, ApiResponse, ApiTags } from ''@nestjs/swagger'';';\" ^\n"    
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" 'import { "+entity_name.capitalize()+"Service } from ''./"+entity_name.lower()+".service'';';\" ^\n" 
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" 'import { Create"+entity_name.capitalize()+"Dto } from ''./dto/create-"+entity_name.lower()+".dto'';';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" 'import { Update"+entity_name.capitalize()+"Dto } from ''./dto/update-"+entity_name.lower()+".dto'';';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '@Controller(''"+entity_name.lower()+"'')';\" ^\n"  
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '@ApiTags(''"+entity_name.capitalize()+"'')';\" ^\n"   
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" 'export class "+entity_name.capitalize()+"Controller {';\" ^\n"   
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" 'constructor(private readonly "+entity_name.lower()+"Service: "+entity_name.capitalize()+"Service) { }';\" ^\n" 
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '@Post()';\" ^\n"   
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '@UsePipes(new ValidationPipe())';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '@ApiOperation({ summary: ''Create "+entity_name.capitalize()+"'' })';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '@ApiBody({ type: Create"+entity_name.capitalize()+"Dto })';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" 'create(@Body() create"+entity_name.capitalize()+"Dto: Create"+entity_name.capitalize()+"Dto) {';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '   return this."+entity_name.lower()+"Service.create(create"+entity_name.capitalize()+"Dto);';\" ^\n" 
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '}';\" ^\n"  
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '@Get()';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '@ApiOperation({ summary: ''Find All "+entity_name.capitalize()+"'' })';\" ^\n"  
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" 'findAll() {';\" ^\n" 
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '   return this."+entity_name.lower()+"Service.findAll();';\" ^\n" 
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '}';\" ^\n"
        atpk = ''
        dt = ''
        for attribute in attributes:
            is_pk = attribute.get("is-pk")
            if is_pk:  
                atpk = attribute.get("name").lower()
                data_type = attribute.get("data-type")
                pk = attribute.get("name").lower()
                data_type_switch = {
                            'INT': "number",
                            'VARCHAR': "string",
                            'FLOAT': "number"
                }
                dt = data_type_switch.get(data_type, "") 
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '@Get('':"+atpk+"'')';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '@ApiOperation({ summary: ''Find One "+entity_name.capitalize()+"'' })';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '@UsePipes(new ValidationPipe())';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" 'findOne(@Param('':"+atpk+"'') id: "+dt+") {';\" ^\n"  
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '   return this."+entity_name.lower()+"Service.findOne(+id);';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '}';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '@Put('':"+atpk+"'')';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '@UsePipes(new ValidationPipe())';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '@ApiOperation({ summary: ''Update "+entity_name.capitalize()+"'' })';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '@ApiBody({ type: Update"+entity_name.capitalize()+"Dto })';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" 'update(@Param('':"+atpk+"'') id: "+dt+", @Body() update"+entity_name.capitalize()+"Dto: Update"+entity_name.capitalize()+"Dto) {';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '   return this."+entity_name.lower()+"Service.update(+id, update"+entity_name.capitalize()+"Dto);';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '}';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '@Delete('':"+atpk+"'')';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '@ApiOperation({ summary: ''Delete "+entity_name.capitalize()+"'' })';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '@UsePipes(new ValidationPipe())';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" 'remove(@Param('':"+atpk+"'') id: "+dt+") {';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '   return this."+entity_name.lower()+"Service.remove(+id);';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '}';\" ^\n"
        codeController += f"    \"Add-Content -Path '{entity_name.lower()}.controller.ts' -Value"+" '}';\" ^\n"
        return codeController
    
    def main_swagger(self, port):
        codeMain = '@echo off\npowershell -Command ^\n'
        codeMain += f"    \"Set-Content -Path 'main.ts' -Value $null;\" ^\n"
        codeMain += f"    \"Add-Content -Path 'main.ts' -Value"+" 'import { NestFactory, Reflector } from ''@nestjs/core'';';\" ^\n"
        codeMain += f"    \"Add-Content -Path 'main.ts' -Value"+" 'import { AppModule } from ''./app.module'';';\" ^\n"
        codeMain += f"    \"Add-Content -Path 'main.ts' -Value"+" 'import { ClassSerializerInterceptor } from ''@nestjs/common'';';\" ^\n"
        codeMain += f"    \"Add-Content -Path 'main.ts' -Value"+" 'import { SwaggerModule, DocumentBuilder } from ''@nestjs/swagger'';';\" ^\n"
        codeMain += f"    \"Add-Content -Path 'main.ts' -Value"+" 'async function bootstrap() {';\" ^\n"
        codeMain += f"    \"Add-Content -Path 'main.ts' -Value"+" '   const app = await NestFactory.create(AppModule);';\" ^\n"
        codeMain += f"    \"Add-Content -Path 'main.ts' -Value"+" '   const config = new DocumentBuilder()';\" ^\n"
        codeMain += f"    \"Add-Content -Path 'main.ts' -Value"+f" '  .setTitle(''Api Rest {(self.PROJECT_NAME).capitalize()}'')';\" ^\n"
        codeMain += f"    \"Add-Content -Path 'main.ts' -Value"+f" '  .setDescription(''Api Rest - {(self.PROJECT_NAME).capitalize()}'')';\" ^\n"
        codeMain += f"    \"Add-Content -Path 'main.ts' -Value"+f" '  .setVersion(''{self.VERSION}'')';\" ^\n"
        codeMain += f"    \"Add-Content -Path 'main.ts' -Value"+f" '  .build();';\" ^\n"
        codeMain += f"    \"Add-Content -Path 'main.ts' -Value"+f" '  const document = SwaggerModule.createDocument(app, config);';\" ^\n"
        codeMain += f"    \"Add-Content -Path 'main.ts' -Value"+f" '  SwaggerModule.setup(''api'', app, document);';\" ^\n"
        codeMain += f"    \"Add-Content -Path 'main.ts' -Value"+f" '  app.enableCors();';\" ^\n"
        codeMain += f"    \"Add-Content -Path 'main.ts' -Value"+f" '  app.useGlobalInterceptors(new ClassSerializerInterceptor(app.get(Reflector)));';\" ^\n"
        codeMain += f"    \"Add-Content -Path 'main.ts' -Value"+f" '  await app.listen({port});';\" ^\n"
        codeMain += f"    \"Add-Content -Path 'main.ts' -Value"+" '}';\" ^\n"
        codeMain += f"    \"Add-Content -Path 'main.ts' -Value"+" 'bootstrap();';\" ^\n"
        return codeMain

    def config_Module(self, entity_name):
        codeModule = '@echo off\npowershell -Command ^\n'
        codeModule += f"    \"Set-Content -Path '{entity_name.lower()}.module.ts' -Value $null;\" ^\n"
        codeModule += f"    \"Add-Content -Path '{entity_name.lower()}.module.ts' -Value"+" 'import { Module } from ''@nestjs/common'';';\" ^\n"
        codeModule += f"    \"Add-Content -Path '{entity_name.lower()}.module.ts' -Value"+" 'import { TypeOrmModule } from ''@nestjs/typeorm'';';\" ^\n"
        codeModule += f"    \"Add-Content -Path '{entity_name.lower()}.module.ts' -Value"+" 'import { "+entity_name.capitalize()+"Service } from ''./"+entity_name.lower()+".service'';';\" ^\n"
        codeModule += f"    \"Add-Content -Path '{entity_name.lower()}.module.ts' -Value"+" 'import { "+entity_name.capitalize()+"Controller } from ''./"+entity_name.lower()+".controller'';';\" ^\n"
        codeModule += f"    \"Add-Content -Path '{entity_name.lower()}.module.ts' -Value"+" 'import { "+entity_name.capitalize()+" } from ''./entities/"+entity_name.lower()+".entity'';';\" ^\n"
        codeModule += f"    \"Add-Content -Path '{entity_name.lower()}.module.ts' -Value"+" '@Module({';\" ^\n"
        codeModule += f"    \"Add-Content -Path '{entity_name.lower()}.module.ts' -Value"+" '  imports: [TypeOrmModule.forFeature(["+entity_name.capitalize()+"])],';\" ^\n"
        codeModule += f"    \"Add-Content -Path '{entity_name.lower()}.module.ts' -Value"+" '  controllers: ["+entity_name.capitalize()+"Controller],';\" ^\n"
        codeModule += f"    \"Add-Content -Path '{entity_name.lower()}.module.ts' -Value"+" '  providers: ["+entity_name.capitalize()+"Service],';\" ^\n"
        codeModule += f"    \"Add-Content -Path '{entity_name.lower()}.module.ts' -Value"+" '  exports: ["+entity_name.capitalize()+"Service],';\" ^\n"
        codeModule += f"    \"Add-Content -Path '{entity_name.lower()}.module.ts' -Value"+" '})';\" ^\n"
        codeModule += f"    \"Add-Content -Path '{entity_name.lower()}.module.ts' -Value"+" 'export class "+entity_name.capitalize()+"Module { }';\"\n"
        return codeModule
   
    def produce_service(self, entity_name, attributes: list[dict], relations):
        codeService = '@echo off\npowershell -Command ^\n'
        codeService += f"    \"Set-Content -Path '{entity_name.lower()}.service.ts' -Value $null;\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" 'import { Injectable, NotFoundException } from ''@nestjs/common'';';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" 'import { Repository, DeepPartial } from ''typeorm'';';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" 'import { Create"+entity_name.capitalize()+"Dto } from ''./dto/create-"+entity_name.lower()+".dto'';';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" 'import { Update"+entity_name.capitalize()+"Dto } from ''./dto/update-"+entity_name.lower()+".dto'';';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" 'import { "+ entity_name.capitalize() +" } from ''./entities/"+entity_name.lower()+".entity'';';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" 'import { InjectRepository } from ''@nestjs/typeorm'';';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '@Injectable()';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" 'export class "+entity_name.capitalize()+"Service {';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" 'constructor(@InjectRepository("+entity_name.capitalize()+")private "+entity_name.lower()+"Repo: Repository<"+entity_name.capitalize()+">,){ }';\" ^\n"
        #Create Service
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" ' async create(data: Create"+entity_name.capitalize()+"Dto){';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '     try{';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '         const newObject = this."+entity_name.lower()+"Repo.create(data);';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '         return {';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '             statusCode: 201,';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '             message: ''Create'',';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '             response: await this."+entity_name.lower()+"Repo.save(newObject)';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '             }';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '     }catch(error) {';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '         return {';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '             statusCode: 500,';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '             message: ''Error Interno'' ';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '             }';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '     }';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" ' }';\" ^\n"
        #Find all Service
        listfk = ''
        for relation in relations:
            listfk += f'\'\'fk_{relation.get("table").lower()}_{entity_name.lower()}\'\','
            
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" ' async findAll(){ return await this."+entity_name.lower()+"Repo.find({relations: ["+listfk+"] });}';\" ^\n"
        #Find
        pk = ''
        data_type = ''
        
        for attribute in attributes:
            is_pk = attribute.get("is-pk")
            if is_pk:
                
                data_type = attribute.get("data-type")
                pk = attribute.get("name").lower()
                data_type_switch = {
                            'INT': f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" ' async findOne("+pk+": number){ return await this."+entity_name.lower()+"Repo.find({where:{ "+pk+": "+pk+"}, relations: ["+listfk+"] });}';\" ^\n",
                            'VARCHAR': f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" ' async findOne("+pk+": string){ return await this."+entity_name.lower()+"Repo.find({where:{ "+pk+": "+pk+"}, relations: ["+listfk+"] });}';\" ^\n",
                            'FLOAT': f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" ' async findOne("+pk+": number){ return await this."+entity_name.lower()+"Repo.find({where:{ "+pk+": "+pk+"}, relations: ["+listfk+"] });}';\" ^\n"
                }
                codeService += data_type_switch.get(data_type, "") 
        
        #Update 
        data_type_switch2 = {
                            'INT': f"{pk}: number",
                            'VARCHAR': f"{pk}: string",
                            'FLOAT':f"{pk}: number",
                }
        code = data_type_switch2.get(data_type, "")
        
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" ' async update("+code+", data: Update"+entity_name.capitalize()+"Dto){';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '     try{';\" ^\n"  
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '         const upd = await this."+entity_name.lower()+"Repo.findOne({where:{ "+pk+": "+pk+"} });';\" ^\n"  
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '         if(upd){';\" ^\n"  
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '             await this."+entity_name.lower()+"Repo.merge(upd, data);';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '             return {';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '                 statusCode: 201,';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '                 message: ''Update'',';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '                 response: await this."+entity_name.lower()+"Repo.save(upd)';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '             }';\" ^\n"   
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '          }else{';\" ^\n" 
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '             return {';\" ^\n" 
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '                 statusCode: 200,';\" ^\n" 
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '                 message: ''Not Found'' ';\" ^\n" 
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '                 }';\" ^\n" 
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '           }';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '      }catch(error) { return { statusCode: 500, message: ''Error Interno''} }';\" ^\n"  
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" ' }';\" ^\n"
               
        #Delete
        
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" ' async remove("+code+"){';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '     try{';\" ^\n"  
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '         const dlt = await this."+entity_name.lower()+"Repo.findOne({where:{ "+pk+": "+pk+"} });';\" ^\n"  
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '         if(dlt){';\" ^\n"  
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '             await this."+entity_name.lower()+"Repo.delete(dlt);';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '             return {';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '                 statusCode: 200,';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '                 message: ''Delete'',';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '             }';\" ^\n"   
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '          }else{';\" ^\n" 
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '             return {';\" ^\n" 
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '                 statusCode: 200,';\" ^\n" 
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '                 message: ''Not Found'' ';\" ^\n" 
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '                 }';\" ^\n" 
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '           }';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '      }catch(error) { return { statusCode: 500, message: ''Error Interno''} }';\" ^\n"  
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" ' }';\" ^\n"
        codeService += f"    \"Add-Content -Path '{entity_name.lower()}.service.ts' -Value"+" '}';\" ^\n" 
        
        
        return codeService  
        
    def produce_dto(self, entity_name, attributes: list[dict], relations):
        codeDto = '@echo off\npowershell -Command ^\n'
        codeDto += f"    \"Set-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value $null;\" ^\n"
        codeDto += f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value"+" 'import { IsString, IsNumber, IsNotEmpty, IsPositive, IsBoolean, IsBooleanString, IsDate, IsEmpty, IsOptional, Min} from ''class-validator'';';\" ^\n"
        codeDto += f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value"+" 'import { Transform, TransformFnParams } from ''class-transformer'';';\" ^\n"
        codeDto += f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value"+" 'import { PartialType } from ''@nestjs/mapped-types'';';\" ^\n"
        codeDto += f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value"+" 'import { ApiProperty } from ''@nestjs/swagger'';';\" ^\n"   
        for relation in relations:
            codeDto += f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value"+" 'import { "+relation.get("table").capitalize()+" } from ''"+f"src/{relation.get("table").lower()}/entities/{relation.get("table").lower()}.entity"+"'';';\" ^\n"
        codeDto += f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value"+" 'function stringToDate({ value }: TransformFnParams) {return new Date(value);}';\" ^\n"
        codeDto += f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value"+f" 'export class Create{entity_name.capitalize()}Dto "+" { ';\" ^\n"
        for attribute in attributes:
            attribute_name = attribute.get("name").lower()
            is_pk = attribute.get("is-pk")
            is_fk = attribute.get("is-fk")
            nn = attribute.get("nn")
            uq = attribute.get("uq")
            ai = attribute.get("ai")
            data_type = attribute.get("data-type")
            
            if is_pk == False:
                codeDto += f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value"+" '    @ApiProperty()';\" ^\n"
                if nn:
                    codeDto += f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value"+" '    @IsNotEmpty()';\" ^\n"
                
                data_type_switch = {
                    'INT': f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value '    @IsNumber()';\" ^\n",
                    'VARCHAR': f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value '    @IsString()';\" ^\n",
                    'FLOAT': f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value '    @IsNumber()';\" ^\n", 
                    'BOOL': f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value '    @IsBoolean()';\" ^\n",
                    'BINARY': f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value '    @IsBoolean()';\" ^\n",
                    'DATE': f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value '    @IsDate()';\" ^\n",
                    'DATETIME': f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value '     @IsDate()';\" ^\n"
                }
                codeDto += data_type_switch.get(data_type, "")
                
                data_type_switch = {
                    'DATE': f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value '    @Transform(stringToDate)';\" ^\n",
                    'DATETIME': f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value '     @Transform(stringToDate)';\" ^\n"
                }
                codeDto += data_type_switch.get(data_type, "")
                
                data_type_switch = {
                    'INT': f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value '    {attribute_name}:number;';\" ^\n",
                    'VARCHAR': f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value '    {attribute_name}:string;';\" ^\n",
                    'FLOAT': f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value '    {attribute_name}:number;';\" ^\n", 
                    'BOOL': f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value '    {attribute_name}:boolean;';\" ^\n",
                    'BINARY': f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value '    {attribute_name}:boolean;\" ^\n",
                    'DATE': f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value '    {attribute_name}:Date;';\" ^\n",
                    'DATETIME': f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value '     {attribute_name}:Date;';\" ^\n"
                }
                codeDto += data_type_switch.get(data_type, "")
        for relation in relations:
            codeDto += f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value"+" '    @IsNotEmpty()';\" ^\n"
            codeDto += f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value"+f" '    fk_{relation.get("table").lower()}_{entity_name.lower()}:{relation.get("table").capitalize()}';\" ^\n"
        codeDto += f"    \"Add-Content -Path 'create-{entity_name.lower()}.dto.ts' -Value"+" '}';\" ^\n"
            
        return codeDto
      
    def produce_entity(self, entity_name, attributes: list[dict], relations, dependencies):
        codeEntity = '@echo off\npowershell -Command ^\n'
        codeEntity += f"    \"Set-Content -Path '{entity_name.lower()}.entity.ts' -Value $null;\" ^\n" 
        codeEntity += f"    \"Add-Content -Path '{entity_name.lower()}.entity.ts' -Value"+" 'import { Column, Entity, PrimaryGeneratedColumn, ManyToOne, OneToMany, JoinColumn} from ''typeorm'';';\" ^\n"
        for dependence in dependencies:
            codeEntity += f"    \"Add-Content -Path '{entity_name.lower()}.entity.ts' -Value"+" 'import { "+dependence.get("table").capitalize()+" } from ''"+f"src/{dependence.get("table").lower()}/entities/{dependence.get("table").lower()}.entity"+"'';';\" ^\n"
        for relation in relations:
            codeEntity += f"    \"Add-Content -Path '{entity_name.lower()}.entity.ts' -Value"+" 'import { "+relation.get("table").capitalize()+" } from ''"+f"src/{relation.get("table").lower()}/entities/{relation.get("table").lower()}.entity"+"'';';\" ^\n"
        codeEntity += f"    \"Add-Content -Path '{entity_name.lower()}.entity.ts' -Value '@Entity()';\" ^\n"
        codeEntity += f"    \"Add-Content -Path '{entity_name.lower()}.entity.ts'"+f" -Value 'export class {entity_name.capitalize()} "+"{';\" ^\n"
        attributesCode = ''
       
        entity_name_lower = entity_name.lower()
        for attribute in attributes:
            attribute_name = attribute.get("name").lower()
            is_pk = attribute.get("is-pk")
            is_fk = attribute.get("is-fk")
            nn = attribute.get("nn")
            uq = attribute.get("uq")
            ai = attribute.get("ai")
            data_type = attribute.get("data-type")
            if is_pk:
                attributesCode += f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '    @PrimaryGeneratedColumn()';\" ^\n"
                data_type_switch = {
                    'INT': f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '    {attribute_name}: number;';\" ^\n",
                    'VARCHAR': f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '    {attribute_name}: string;';\" ^\n",
                    'FLOAT': f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '    {attribute_name}: number;';\" ^\n", 
                    'BOOL': f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '    {attribute_name}: boolean;';\" ^\n",
                    'BINARY': f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '    {attribute_name}: boolean;';\" ^\n",
                    'DATE': f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '    {attribute_name}: Date;';\" ^\n",
                    'DATETIME': f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '    {attribute_name}: Date;';\" ^\n"
                }
                attributesCode += data_type_switch.get(data_type, "")
        
            else:
                data_type_switch = {
                    'INT': (
                        f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '"+"    @Column({ type: ''integer'', "+f"unique: {uq}, nullable: {nn}"+"})';\" ^\n"
                        f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '    {attribute_name}: number;';\" ^\n"
                    ),
                    'VARCHAR': (
                        f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '"+"    @Column({ type: ''varchar'', length: 50, "+f"unique: {uq}, nullable: {nn}"+" })';\" ^\n"
                        f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '    {attribute_name}: string;';\" ^\n"
                    ),
                    'FLOAT': (
                        f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '"+"    @Column({ type: ''float'',"+f"unique: {uq}, nullable: {nn}"+"})';\" ^\n"
                        f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '    {attribute_name}: number;';\" ^\n"
                    ),
                    'BOOL': (
                        f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '"+"    @Column({ type: ''boolean'', "+f"unique: {uq}, nullable: {nn}"+"})';\" ^\n"
                        f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '    {attribute_name}: boolean;';\" ^\n"
                    ),
                    'BINARY': (
                        f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '"+"    @Column({ type: ''binary''"+f"unique: {uq}, nullable: {nn}"+"})';\" ^\n"
                        f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '    {attribute_name}: boolean;';\" ^\n"
                    ),
                    'DATE': (
                        f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '"+"    @Column({ type: ''date'', "+f"unique: {uq}, nullable: {nn}"+"})';\" ^\n"
                        f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '    {attribute_name}: Date;';\" ^\n"
                    ),
                    'DATETIME': (
                        f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '"+"    @Column({ type: ''datetime'', "+f"unique: {uq}, nullable: {nn}"+"})';\" ^\n"
                        f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '    {attribute_name}: Date;';\" ^\n"
                    )
                }
            
                attributesCode += data_type_switch.get(data_type, "")
        codeEntity += attributesCode
        for relation in relations:
            codeEntity += f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '"+"    @ManyToOne(() => "+ f"{relation.get("table").capitalize()}, ({relation.get("table").lower()}) => {relation.get("table").lower()}.{entity_name.lower()}," + " {';\" ^\n"
            codeEntity += f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '    nullable: false,';\" ^\n"
            codeEntity += f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '    "+"})';\" ^\n"
            codeEntity += f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '    @JoinColumn("+"{"+f" name: ''fk_{relation.get("table").lower()}_{entity_name.lower()}''"+" })';\" ^\n"
            codeEntity += f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '    fk_{relation.get("table").lower()}_{entity_name.lower()}: {relation.get("table").capitalize()};';\" ^\n"
        for dependence in dependencies:
            codeEntity += f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '    @OneToMany(()"+f" => {dependence.get("table").capitalize()}, ({dependence.get("table").lower()}) => {dependence.get("table").lower()}.fk_{entity_name.lower()}_{dependence.get("table").lower()})';\" ^\n"
            codeEntity += f"    \"Add-Content -Path '{entity_name_lower}.entity.ts' -Value '    {dependence.get("table").lower()}: {dependence.get("table").capitalize()}[];';\" ^\n"
        codeEntity += f"    \"Add-Content -Path '{entity_name.lower()}.entity.ts'"+" -Value '}'\"\n"
        return codeEntity
    
    def produce_app_file(self, entities):
        # self.script_method.add_cd("..")
        self.script_method.add_command(f"npm i @nestjs/typeorm typeorm sqlite3")
        self.script_method.add_comment("Crear la base de datos con un script de Python incluido en el archivo .bat")
        self.script_method.add_print("Creando la base de datos SQLite...")
        # self.script_method.add_cd('src')
        
        #Creando conexión
        # self._script.add(f"    \"Set-Content -Path 'app.module.ts' -Value $null;\" ^")
        self._script.add("import { Module } from '@nestjs/common';")
        self._script.add("import { AppController } from './app.controller';")
        self._script.add("import { AppService } from './app.service';")
        self._script.add("import { TypeOrmModule } from '@nestjs/typeorm';")

        listentities = ''
        listModules = ''
        for entity in entities:
            listentities += f"{entity.capitalize()},"
            listModules += f"{entity.capitalize()}Module,"
            self._script.add(f"import {entity.capitalize()}Module from './{entity.lower()}/{entity.lower()}.module';")
            self._script.add(f"import {entity.capitalize()} from './{entity.lower()}/entities/{entity.lower()}.entity';")
        self._script.add("\n")
        self._script.add(f"@Module({"{"}")
        self._script.add(f"    imports: [TypeOrmModule.forRoot({type: ''sqlite'', database: ''database.sqlite'',entities: ["+listentities+"], synchronize: true, }), TypeOrmModule.forFeature(["+listentities+"]), "+listModules+"],';\" ^")
        self._script.add("        type: 'sqlite',")
        self._script.add("        database: 'database.sqlite',")
        self._script.add(f"        entities: [{listentities}],")
        self._script.add(f"        synchronize: true")
        self._script.add(f"    {"}"}),")
        self._script.add(f"    {"}"}),")
        self._script.add(f"controllers: [AppController],';\" ^")
        self._script.add(f"providers: [AppService],';\" ^")
        self._script.add(f"})';\" ^")
        self._script.add(f"export class AppModule { }';\"")
        #Config main.ts
        codeMain = self.main_swagger(port)
        self.script_method.add_command(codeMain)
        self.script_method.add_cd('..')
        self.script_method.add_powerShellCommand(f"Start-Process cmd -ArgumentList '/c npm i class-validator' -NoNewWindow -Wait")
        self.script_method.add_powerShellCommand(f"Start-Process cmd -ArgumentList '/c npm i class-transformer' -NoNewWindow -Wait")
        self.script_method.add_powerShellCommand(f"Start-Process cmd -ArgumentList '/c npm i @nestjs/mapped-types' -NoNewWindow -Wait") 
        self.script_method.add_powerShellCommand(f"Start-Process cmd -ArgumentList '/c npm i @nestjs/swagger' -NoNewWindow -Wait")  
        self.script_method.add_powerShellCommand(f"Start-Process cmd -ArgumentList '/c npm run start:dev' -NoNewWindow -Wait") 
        self.script_method.add_pause()
