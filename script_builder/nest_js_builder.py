from .utils.data_types_nest_js import get_javascript_type, get_validator_type, type_to_valid_type_orm_type
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
    
    def produce_crud(self, entity_name: str, attributes: list[dict], relations: list[dict], dependencies: list[dict]):
        self.script_method.add_comment(f"Creando modulo {entity_name.lower()}...")
        self.script_method.add_print(f"Creando modulo {entity_name.lower()}...")
        self.script_method.add_command(f"nest generate resource {entity_name.lower()}")
        #Create entity
        # self.script_method.add_cd(entity_name.lower())
        # self.script_method.add_cd("entities")
        self.produce_entity(entity_name, attributes, relations, dependencies)
        # self.script_method.add_cd("..")
        # self.script_method.add_cd("..")
        #Create dto
        # self.script_method.add_cd(entity_name.lower())
        # self.script_method.add_cd("dto")
        self.produce_dto(entity_name, attributes, relations)
        # self.script_method.add_cd("..")
        # self.script_method.add_cd("..")
        #Create service
        # self.script_method.add_cd(entity_name.lower())
        self.produce_service(entity_name, attributes, relations, dependencies)
        # self.script_method.add_command(codeService)
        # self.script_method.add_cd("..")
        # self.script_method.add_cd("..")
        #Config modules
        self.script_method.add_cd(entity_name.lower())
        codeModule = self.config_Module( entity_name, attributes, relations, dependencies)
        self.script_method.add_command(codeModule)
        #Create Controller
        codeController = self.produce_controller( entity_name, attributes, relations, dependencies)
        self.script_method.add_command(codeController)
        self.script_method.add_cd("..")
        self.script_method.add_cd("..")
        
    def produce_entity(self, entity_name: str, attributes: list[dict], relations: list[dict], dependencies: list[dict]) -> None:
        self._script.add("import { Column, Entity, PrimaryGeneratedColumn, ManyToOne, OneToMany, JoinColumn} from 'typeorm';")
        aux_path: str = ""
        for dependence in dependencies:
            aux_path = f"src/{dependence.get("table").lower()}/entities/{dependence.get("table").lower()}.entity"
            self._script.add(f"import {"{"}{dependence.get("table").capitalize()}{"}"} from '{aux_path}';")
        for relation in relations:
            aux_path = f"src/{relation.get("table").lower()}/entities/{relation.get("table").lower()}.entity"
            self._script.add(f"import {"{"} {relation.get("table").capitalize()} {"}"} from '{aux_path}';")
        self._script.add("\n")

        self._script.add("@Entity();")
        self._script.add(f"export class {entity_name.capitalize()} {"{"}")
        for attribute in attributes:
            attribute_name = attribute.get("name").lower()
            is_pk = attribute.get("is-pk")
            nn = attribute.get("nn")
            uq = attribute.get("uq")
            data_type = attribute.get("data-type")
            if is_pk:
                self._script.add("    @PrimaryGeneratedColumn()")        
            else:
                self._script.add(f"    @Column({"{"} type: '{type_to_valid_type_orm_type(data_type)}', unique: {uq}, nullable: {nn}{"}"})")
            self._script.add(f"    {attribute_name}: {get_javascript_type(data_type)};")
                
        entity_name_lower = entity_name.lower()
        aux_table: str = ""
        aux_table_lower: str = ""
        aux_table_capitalize: str = ""
        aux_attribute_relation: str = ""
        
        for relation in relations:
            aux_table = relation.get("table")
            aux_table_lower = aux_table.lower()
            aux_table_capitalize = aux_table.capitalize()
            self._script.add(f"    @ManyToOne(() => {aux_table_capitalize}, ({aux_table_lower}) => {aux_table_lower}.{entity_name_lower}, {"{"}")
            self._script.add("        nullable: false,")
            self._script.add("    })")

            aux_attribute_relation = f'fk_{aux_table_lower}_{entity_name_lower}'
            self._script.add(f"    @JoinColumn({"{"} name: '{aux_attribute_relation}'{"}"})")
            self._script.add(f"    {aux_attribute_relation}: {aux_table_capitalize};")

        for dependence in dependencies:
            aux_table = dependence.get("table")
            aux_table_lower = aux_table.lower()
            aux_table_capitalize = aux_table.capitalize()
            aux_attribute_relation = f'fk_{entity_name_lower}_{aux_table_lower}'
            self._script.add(f"    @OneToMany(() => {aux_table_capitalize}, ({aux_table_lower}) => {aux_table_lower}.{aux_attribute_relation})")
            self._script.add(f"    {aux_table_lower}: {aux_table_capitalize}[];")
        
        self._script.add("}")
        self._script.add("\n")
        self.script_method.add_write_to_file(f"{entity_name_lower}/entities/{entity_name_lower}.entity.ts", self._script)
        self._script.reset_parts()
        self.script_method.add_line_break()

    def produce_dto(self, entity_name, attributes: list[dict], relations: list[dict]) -> None:
        self._script.add("import { IsString, IsNumber, IsNotEmpty, IsPositive, IsBoolean, IsBooleanString, IsDate, IsEmpty, IsOptional, Min} from 'class-validator';")
        self._script.add("import { Transform, TransformFnParams } from 'class-transformer';")
        self._script.add("import { PartialType } from '@nestjs/mapped-types';")
        self._script.add("import { ApiProperty } from '@nestjs/swagger';")
        
        aux_table: str = ""
        for relation in relations:
            aux_table = relation.get("table")
            self._script.add(f"import {"{"} {aux_table.capitalize()} {"}"} from 'src/{aux_table.lower()}/entities/{aux_table.lower()}.entity';")
        
        self._script.add("\n")
        self._script.add("function stringToDate({ value }: TransformFnParams) {")
        self._script.add("    return new Date(value);")
        self._script.add("}")
        self._script.add("\n")

        self._script.add(f"export class Create{entity_name.capitalize()}Dto {"{"}")
        for attribute in attributes:
            is_pk = attribute.get("is-pk")
            if is_pk:
                continue

            attribute_name = attribute.get("name").lower()
            nn = attribute.get("nn")
            data_type = attribute.get("data-type")
            
            self._script.add("    @ApiProperty()")
            if nn:
                self._script.add("    @IsNotEmpty()")
            self._script.add(f"    @{get_validator_type(data_type)}()")
            if data_type=="DATE" or data_type=="DATETIME":
                self._script.add("    @Transform(stringToDate)")
            self._script.add(f"    {attribute_name}:{get_javascript_type(data_type)};")
        
        entity_name_lower = entity_name.lower()
        aux_attribute_relation: str = ""
        aux_table_relation: str = ""
        for relation in relations:
            aux_table = relation.get("table")
            aux_attribute_relation = f"fk_{aux_table.lower()}_{entity_name_lower}"
            aux_table_relation = f"{aux_table.capitalize()}"
            self._script.add("    @IsNotEmpty()")
            self._script.add(f"    {aux_attribute_relation}: {aux_table_relation};")
        self._script.add("}")
        self._script.add("\n")
        
        self.script_method.add_write_to_file(f"{entity_name_lower}/dto/create-{entity_name_lower}.dto.ts", self._script)
        self._script.reset_parts()
        self.script_method.add_line_break()

    def produce_service(self, entity_name, attributes: list[dict], relations: list[dict]) -> None:
        entity_capitalize: str = entity_name.capitalize()
        entity_lower: str = entity_name.lower()

        self._script.add("import { Injectable, NotFoundException } from '@nestjs/common';")
        self._script.add("import { Repository, DeepPartial } from 'typeorm';")
        self._script.add(f"import {"{"} Create{entity_capitalize}Dto {"}"} from './dto/create-{entity_lower}.dto';")
        self._script.add(f"import {"{"} Update{entity_capitalize}Dto {"}"} from './dto/update-{entity_lower}.dto';")
        self._script.add(f"import {"{"} {entity_capitalize} {"}"} from './entities/{entity_lower}.entity';")
        self._script.add("import { InjectRepository } from '@nestjs/typeorm';")
        self._script.add("\n")
        self._script.add("@Injectable()")
        self._script.add(f"export class {entity_capitalize}Service {"{"}")
        self._script.add("    constructor(")
        self._script.add(f"        @InjectRepository({entity_capitalize}) private {entity_lower}Repo: Repository<{entity_capitalize}>,")
        self._script.add("    ) {}")
        self._script.add("\n")
        
        pk_attribute: str = ""
        for attribute in attributes:
            if attribute.get("is-pk"):
                pk_attribute = attribute.get("name").lower()
        self.produce_create(entity_capitalize, entity_lower)
        self.produce_read(relations, entity_lower, pk_attribute)
        self.produce_update(entity_lower, entity_capitalize, pk_attribute)
        self.produce_delete(entity_lower, pk_attribute)
        self._script.add("}")
        self._script.add("\n")

        self.script_method.add_write_to_file(f"{entity_lower}/{entity_lower}.service.ts", self._script)
        self._script.reset_parts()
        self.script_method.add_line_break()
        
    def produce_create(self, entity_capitalize: str, entity_lower: str) -> None:
        self._script.add(f"    async create(data: Create{entity_capitalize}Dto) {"{"}")
        self._script.add("        try {")
        self._script.add(f"            const newObject = this.{entity_lower}Repo.create(data);")
        self._script.add("            return {")
        self._script.add("                statusCode: 201,")
        self._script.add("                message: 'Create',")
        self._script.add(f"                response: await this.{entity_lower}Repo.save(newObject),")
        self._script.add("            };")
        self._script.add("        } catch (error) {")
        self._script.add("            return {")
        self._script.add("                statusCode: 500,")
        self._script.add("                message: 'Error Interno',")
        self._script.add("            };")
        self._script.add("        }")
        self._script.add("    }")
        self._script.add("\n")

    def produce_read(self, relations: list[dict], entity_lower: str, pk_attribute: str) -> None:
        list_fk = ''
        for relation in relations:
            list_fk += f"'fk_{relation.get("table").lower()}_{entity_lower}', "
        
        self._script.add("    async findAll() {")
        self._script.add(f"        return await this.{entity_lower}Repo.find({"{"}relations: [{list_fk}] {"}"})")
        self._script.add("    }")
        self._script.add("\n")
        self._script.add(f"    async findOne({pk_attribute}: number) {"{"}")
        self._script.add(f"        return await this.{entity_lower}Repo.find({"{"}")
        self._script.add(f"            where: {"{"} {pk_attribute}: {pk_attribute} {"}"},")
        self._script.add(f"            relations: [{list_fk}],")
        self._script.add("        }")
        self._script.add("    }")
        self._script.add("\n")

    def produce_update(self, entity_lower: str, entity_capitalize: str, pk_attribute: str) -> None:
        self._script.add(f"    async update({pk_attribute}: number, data: Update{entity_capitalize}Dto) {"{"}")
        self._script.add("        try {")
        self._script.add(f"            const upd = await this.{entity_lower}Repo.findOne({"{"}")
        self._script.add(f"                where: {"{"} {pk_attribute}: {pk_attribute} {"}"},")
        self._script.add("            });")
        self._script.add("            if (upd) {")
        self._script.add(f"                await this.{entity_lower}Repo.merge(upd, data);")
        self._script.add("                return {")
        self._script.add("                    statusCode: 201,")
        self._script.add("                    message: 'Update',")
        self._script.add(f"                    response: await this.{entity_lower}Repo.save(upd),")
        self._script.add("                };")
        self._script.add("            } else {" )
        self._script.add("                return {" )
        self._script.add("                    statusCode: 401," )
        self._script.add("                    message: 'Not Found'," )
        self._script.add("                };" )
        self._script.add("            }")
        self._script.add("        } catch (error) {")
        self._script.add("            return { statusCode: 500, message: 'Error Interno' };")
        self._script.add("        }")
        self._script.add("    }")
        self._script.add("\n")

    def produce_delete(self, entity_lower: str, pk_attribute: str) -> None:
        self._script.add(f"    async remove({pk_attribute}: number) {"{"}")
        self._script.add("        try {"  )
        self._script.add(f"            const dlt = await this.{entity_lower}Repo.findOne({"{"}")
        self._script.add(f"                where: {"{"} {pk_attribute}: {pk_attribute} {"}"},")
        self._script.add("            });")
        self._script.add("            if (dlt) {"  )
        self._script.add(f"                await this.{entity_lower}Repo.delete(dlt);")
        self._script.add("                return {")
        self._script.add("                    statusCode: 200,")
        self._script.add("                    message: 'Delete',")
        self._script.add("                };")
        self._script.add("            } else {")
        self._script.add("                return {" )
        self._script.add("                    statusCode: 401," )
        self._script.add("                    message: 'Not Found',")
        self._script.add("                };")
        self._script.add("            }")
        self._script.add("        } catch (error) {")
        self._script.add("            return { statusCode: 500, message: 'Error Interno' };")
        self._script.add("        }")
        self._script.add("    }")
        self._script.add("\n")

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
    
    def produce_app_file(self, entities):
        # self.script_method.add_cd("..")
        self.script_method.add_comment("Crear la base de datos con un script de Python incluido en el archivo .bat")
        self.script_method.add_print("Creando la base de datos SQLite...")
        # self.script_method.add_cd('src')
        
        #Creando conexión
        self._script.add("import { Module } from '@nestjs/common';")
        self._script.add("import { TypeOrmModule } from '@nestjs/typeorm';")
        self._script.add("\n")
        self._script.add("import { AppController } from './app.controller';")
        self._script.add("import { AppService } from './app.service';")
        self._script.add("\n")

        listentities = ''
        listModules = ''
        for entity in entities:
            listentities += f"{entity.capitalize()},"
            listModules += f"{entity.capitalize()}Module,"
            self._script.add(f"import {entity.capitalize()}Module from './{entity.lower()}/{entity.lower()}.module';")
            self._script.add(f"import {entity.capitalize()} from './{entity.lower()}/entities/{entity.lower()}.entity';")
            self._script.add("\n")
        
        self._script.add("@Module({")
        self._script.add("    imports: [")
        self._script.add("        TypeOrmModule.forRoot({")
        self._script.add("            type: 'sqlite',")
        self._script.add("            database: 'database.sqlite',")
        self._script.add(f"            entities: [{listentities}],")
        self._script.add("            synchronize: true")
        self._script.add("        }),")
        self._script.add(f"        TypeOrmModule.forFeature([{listentities}]),")
        self._script.add(f"        {listentities}")
        self._script.add("    ],")
        self._script.add(f"    controllers: [AppController],")
        self._script.add(f"    providers: [AppService],")
        self._script.add("})")
        self._script.add("export class AppModule { }")
        self._script.add("\n")
        self.script_method.add_write_to_file("src/app.module.ts", self._script)
        self._script.reset_parts()
        self.script_method.add_line_break()

        #Config main.ts
        self.produce_main_swagger()

        #Execute
        self.script_method.add_command("npm i @nestjs/typeorm typeorm sqlite3")
        self.script_method.add_command("npm i class-validator")
        self.script_method.add_command("npm i class-transformer")
        self.script_method.add_command("npm i @nestjs/mapped-types") 
        self.script_method.add_command("npm i @nestjs/swagger")
        self.script_method.add_command("npm run start:dev") 

    def produce_main_swagger(self) -> None:
        self._script.add("import { NestFactory, Reflector } from '@nestjs/core';")
        self._script.add("import { ClassSerializerInterceptor } from '@nestjs/common';")
        self._script.add("import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';")
        self._script.add("\n")
        self._script.add("import { AppModule } from './app.module';")
        self._script.add("\n")
        self._script.add("async function bootstrap() {")
        self._script.add("    const app = await NestFactory.create(AppModule);")
        self._script.add("\n")
        self._script.add("    const config = new DocumentBuilder()")
        self._script.add(f"        .setTitle('Api Rest {(self.PROJECT_NAME).capitalize()}')")
        self._script.add(f"        .setDescription('Api Rest - {(self.PROJECT_NAME).capitalize()}')")
        self._script.add(f"        .setVersion('0.0.1')")
        self._script.add(f"        .build();")
        self._script.add("\n")
        self._script.add(f"    const document = SwaggerModule.createDocument(app, config);")
        self._script.add("\n")
        self._script.add(f"    SwaggerModule.setup('api', app, document);")
        self._script.add("\n")
        self._script.add(f"    app.enableCors();")
        self._script.add(f"    app.useGlobalInterceptors(new ClassSerializerInterceptor(app.get(Reflector)));")
        self._script.add(f"    await app.listen({NestApiBuilder.EXECUTE_PORT});")
        self._script.add("}")
        self._script.add("\n")
        self._script.add("bootstrap();")
        self._script.add("\n")
        
        self.script_method.add_write_to_file("src/main.ts", self._script)
        self._script.reset_parts()
        self.script_method.add_line_break()
