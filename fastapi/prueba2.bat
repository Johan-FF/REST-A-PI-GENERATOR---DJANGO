@echo off
rem Nombre del proyecto
rem Crear directorio del proyecto
echo Crear directorio del proyecto
set "PROJECT_NAME=TIENDA"
mkdir %PROJECT_NAME%
cd %PROJECT_NAME%
echo .
rem Usar PowerShell para automatizar la creación del proyecto
powershell -Command "Start-Process cmd -ArgumentList '/c nest new %PROJECT_NAME%','--package-manager npm' -NoNewWindow -Wait"
echo .
rem Entrando src...
cd tienda\src
rem Creando modulo cliente...
echo Creando modulo cliente...
powershell -Command "Start-Process cmd -ArgumentList '/c nest generate resource cliente ' -NoNewWindow -Wait"
echo .
cd cliente
cd entities
@echo off
powershell -Command ^
    "Set-Content -Path 'cliente.entity.ts' -Value $null;" ^
    "Add-Content -Path 'cliente.entity.ts' -Value 'import { Column, Entity, PrimaryGeneratedColumn, ManyToOne, OneToMany, JoinColumn} from ''typeorm'';';" ^
    "Add-Content -Path 'cliente.entity.ts' -Value 'import { Factura } from ''src/factura/entities/factura.entity'';';" ^
    "Add-Content -Path 'cliente.entity.ts' -Value '@Entity()';" ^
    "Add-Content -Path 'cliente.entity.ts' -Value 'export class Cliente {';" ^
    "Add-Content -Path 'cliente.entity.ts' -Value '    @PrimaryGeneratedColumn()';" ^
    "Add-Content -Path 'cliente.entity.ts' -Value '    id_cliente: number;';" ^
    "Add-Content -Path 'cliente.entity.ts' -Value '    @Column({ type: ''varchar'', length: 50, unique: false, nullable: true })';" ^
    "Add-Content -Path 'cliente.entity.ts' -Value '    name: string;';" ^
    "Add-Content -Path 'cliente.entity.ts' -Value '    @Column({ type: ''boolean'', unique: false, nullable: true})';" ^
    "Add-Content -Path 'cliente.entity.ts' -Value '    activate: boolean;';" ^
    "Add-Content -Path 'cliente.entity.ts' -Value '    @OneToMany(() => Factura, (factura) => factura.cliente)';" ^
    "Add-Content -Path 'cliente.entity.ts' -Value '    factura: Factura[];';" ^
    "Add-Content -Path 'cliente.entity.ts' -Value '}'"

cd ..
cd ..
cd cliente
cd dto
@echo off
powershell -Command ^
    "Set-Content -Path 'create-cliente.dto.ts' -Value $null;" ^
    "Add-Content -Path 'create-cliente.dto.ts' -Value 'import { IsString, IsNumber, IsNotEmpty, IsPositive, IsBoolean, IsBooleanString, IsDate, IsEmpty, IsOptional, Min} from ''class-validator'';';" ^
    "Add-Content -Path 'create-cliente.dto.ts' -Value 'import { Transform, TransformFnParams } from ''class-transformer'';';" ^
    "Add-Content -Path 'create-cliente.dto.ts' -Value 'import { PartialType } from ''@nestjs/mapped-types'';';" ^
    "Add-Content -Path 'create-cliente.dto.ts' -Value 'function stringToDate({ value }: TransformFnParams) {return new Date(value);}';" ^
    "Add-Content -Path 'create-cliente.dto.ts' -Value 'export class CreateClienteDto  { ';" ^
    "Add-Content -Path 'create-cliente.dto.ts' -Value '    @IsNotEmpty()';" ^
    "Add-Content -Path 'create-cliente.dto.ts' -Value '    @IsString()';" ^
    "Add-Content -Path 'create-cliente.dto.ts' -Value '    name:string;';" ^
    "Add-Content -Path 'create-cliente.dto.ts' -Value '    @IsNotEmpty()';" ^
    "Add-Content -Path 'create-cliente.dto.ts' -Value '    @IsBoolean()';" ^
    "Add-Content -Path 'create-cliente.dto.ts' -Value '    activate:boolean;';" ^
    "Add-Content -Path 'create-cliente.dto.ts' -Value '}';" ^

cd ..
cd ..
cd cliente
@echo off
powershell -Command ^
    "Set-Content -Path 'cliente.service.ts' -Value $null;" ^
    "Add-Content -Path 'cliente.service.ts' -Value 'import { Injectable, NotFoundException } from ''@nestjs/common'';';" ^
    "Add-Content -Path 'cliente.service.ts' -Value 'import { Repository, DeepPartial } from ''typeorm'';';" ^
    "Add-Content -Path 'cliente.service.ts' -Value 'import { CreateClienteDto } from ''./dto/create-cliente.dto'';';" ^
    "Add-Content -Path 'cliente.service.ts' -Value 'import { UpdateClienteDto } from ''./dto/update-cliente.dto'';';" ^
    "Add-Content -Path 'cliente.service.ts' -Value 'import { Cliente } from ''./entities/cliente.entity'';';" ^
    "Add-Content -Path 'cliente.service.ts' -Value 'import { InjectRepository } from ''@nestjs/typeorm'';';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '@Injectable()';" ^
    "Add-Content -Path 'cliente.service.ts' -Value 'export class ClienteService {';" ^
    "Add-Content -Path 'cliente.service.ts' -Value 'constructor(@InjectRepository(Cliente)private clienteRepo: Repository<Cliente>,){ }';" ^
    "Add-Content -Path 'cliente.service.ts' -Value ' async create(data: CreateClienteDto){';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '     try{';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '         const newObject = this.clienteRepo.create(data);';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '         return {';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '             statusCode: 201,';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '             message: ''Create'',';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '             response: await this.clienteRepo.save(newObject)';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '             }';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '     }catch(error) {';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '         return {';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '             statusCode: 500,';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '             message: ''Error Interno'' ';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '             }';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '     }';" ^
    "Add-Content -Path 'cliente.service.ts' -Value ' }';" ^
    "Add-Content -Path 'cliente.service.ts' -Value ' async findAll(){ return await this.clienteRepo.find({relations: [] });}';" ^
    "Add-Content -Path 'cliente.service.ts' -Value ' async findOne(id_cliente: number){ return await this.clienteRepo.find({where:{ id_cliente: id_cliente}, relations: [] });}';" ^
    "Add-Content -Path 'cliente.service.ts' -Value ' async update(id_cliente: number, data: UpdateClienteDto){';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '     try{';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '         const upd = await this.clienteRepo.findOne({where:{ id_cliente: id_cliente} });';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '         if(upd){';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '             await this.clienteRepo.merge(upd, data);';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '             return {';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '                 statusCode: 201,';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '                 message: ''Update'',';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '                 response: await this.clienteRepo.save(upd)';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '             }';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '          }else{';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '             return {';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '                 statusCode: 200,';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '                 message: ''Usuario no encontrado'' ';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '                 }';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '           }';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '      }catch(error) { return { statusCode: 500, message: ''Error Interno''} }';" ^
    "Add-Content -Path 'cliente.service.ts' -Value ' }';" ^
    "Add-Content -Path 'cliente.service.ts' -Value ' async remove(id_cliente: number){';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '     try{';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '         const dlt = await this.clienteRepo.findOne({where:{ id_cliente: id_cliente} });';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '         if(dlt){';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '             await this.clienteRepo.delete(dlt);';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '             return {';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '                 statusCode: 200,';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '                 message: ''Delete'',';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '             }';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '          }else{';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '             return {';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '                 statusCode: 200,';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '                 message: ''Usuario no encontrado'' ';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '                 }';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '           }';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '      }catch(error) { return { statusCode: 500, message: ''Error Interno''} }';" ^
    "Add-Content -Path 'cliente.service.ts' -Value ' }';" ^
    "Add-Content -Path 'cliente.service.ts' -Value '}';" ^

cd ..
cd ..
cd cliente
@echo off
powershell -Command ^
    "Set-Content -Path 'cliente.module.ts' -Value $null;" ^
    "Add-Content -Path 'cliente.module.ts' -Value 'import { Module } from ''@nestjs/common'';';" ^
    "Add-Content -Path 'cliente.module.ts' -Value 'import { TypeOrmModule } from ''@nestjs/typeorm'';';" ^
    "Add-Content -Path 'cliente.module.ts' -Value 'import { ClienteService } from ''./cliente.service'';';" ^
    "Add-Content -Path 'cliente.module.ts' -Value 'import { ClienteController } from ''./cliente.controller'';';" ^
    "Add-Content -Path 'cliente.module.ts' -Value 'import { Cliente } from ''./entities/cliente.entity'';';" ^
    "Add-Content -Path 'cliente.module.ts' -Value '@Module({';" ^
    "Add-Content -Path 'cliente.module.ts' -Value '  imports: [TypeOrmModule.forFeature([Cliente])],';" ^
    "Add-Content -Path 'cliente.module.ts' -Value '  controllers: [ClienteController],';" ^
    "Add-Content -Path 'cliente.module.ts' -Value '  providers: [ClienteService],';" ^
    "Add-Content -Path 'cliente.module.ts' -Value '  exports: [ClienteService],';" ^
    "Add-Content -Path 'cliente.module.ts' -Value '})';" ^
    "Add-Content -Path 'cliente.module.ts' -Value 'export class ClienteModule { }';" ^

cd ..
cd ..
rem Creando modulo factura...
echo Creando modulo factura...
powershell -Command "Start-Process cmd -ArgumentList '/c nest generate resource factura ' -NoNewWindow -Wait"
echo .
cd factura
cd entities
@echo off
powershell -Command ^
    "Set-Content -Path 'factura.entity.ts' -Value $null;" ^
    "Add-Content -Path 'factura.entity.ts' -Value 'import { Column, Entity, PrimaryGeneratedColumn, ManyToOne, OneToMany, JoinColumn} from ''typeorm'';';" ^
    "Add-Content -Path 'factura.entity.ts' -Value 'import { Cliente } from ''src/cliente/entities/cliente.entity'';';" ^
    "Add-Content -Path 'factura.entity.ts' -Value '@Entity()';" ^
    "Add-Content -Path 'factura.entity.ts' -Value 'export class Factura {';" ^
    "Add-Content -Path 'factura.entity.ts' -Value '    @PrimaryGeneratedColumn()';" ^
    "Add-Content -Path 'factura.entity.ts' -Value '    id_factura: number;';" ^
    "Add-Content -Path 'factura.entity.ts' -Value '    @Column({ type: ''date'', unique: false, nullable: true})';" ^
    "Add-Content -Path 'factura.entity.ts' -Value '    fecha: Date;';" ^
    "Add-Content -Path 'factura.entity.ts' -Value '    @ManyToOne(() => Cliente, (cliente) => cliente.factura, {';" ^
    "Add-Content -Path 'factura.entity.ts' -Value '    nullable: false,';" ^
    "Add-Content -Path 'factura.entity.ts' -Value '    })';" ^
    "Add-Content -Path 'factura.entity.ts' -Value '    @JoinColumn({ name: ''fk_cliente_factura'' })';" ^
    "Add-Content -Path 'factura.entity.ts' -Value '    cliente: Cliente;';" ^
    "Add-Content -Path 'factura.entity.ts' -Value '}'"

cd ..
cd ..
cd factura
cd dto
@echo off
powershell -Command ^
    "Set-Content -Path 'create-factura.dto.ts' -Value $null;" ^
    "Add-Content -Path 'create-factura.dto.ts' -Value 'import { IsString, IsNumber, IsNotEmpty, IsPositive, IsBoolean, IsBooleanString, IsDate, IsEmpty, IsOptional, Min} from ''class-validator'';';" ^
    "Add-Content -Path 'create-factura.dto.ts' -Value 'import { Transform, TransformFnParams } from ''class-transformer'';';" ^
    "Add-Content -Path 'create-factura.dto.ts' -Value 'import { PartialType } from ''@nestjs/mapped-types'';';" ^
    "Add-Content -Path 'create-factura.dto.ts' -Value 'import { Cliente } from ''src/cliente/entities/cliente.entity'';';" ^
    "Add-Content -Path 'create-factura.dto.ts' -Value 'function stringToDate({ value }: TransformFnParams) {return new Date(value);}';" ^
    "Add-Content -Path 'create-factura.dto.ts' -Value 'export class CreateFacturaDto  { ';" ^
    "Add-Content -Path 'create-factura.dto.ts' -Value '    @IsNotEmpty()';" ^
    "Add-Content -Path 'create-factura.dto.ts' -Value '    @IsDate()';" ^
    "Add-Content -Path 'create-factura.dto.ts' -Value '    @Transform(stringToDate)';" ^
    "Add-Content -Path 'create-factura.dto.ts' -Value '    fecha:Date;';" ^
    "Add-Content -Path 'create-factura.dto.ts' -Value '    @IsNotEmpty()';" ^
    "Add-Content -Path 'create-factura.dto.ts' -Value '    fk_cliente_factura:Cliente';" ^
    "Add-Content -Path 'create-factura.dto.ts' -Value '}';" ^

cd ..
cd ..
cd factura
@echo off
powershell -Command ^
    "Set-Content -Path 'factura.service.ts' -Value $null;" ^
    "Add-Content -Path 'factura.service.ts' -Value 'import { Injectable, NotFoundException } from ''@nestjs/common'';';" ^
    "Add-Content -Path 'factura.service.ts' -Value 'import { Repository, DeepPartial } from ''typeorm'';';" ^
    "Add-Content -Path 'factura.service.ts' -Value 'import { CreateFacturaDto } from ''./dto/create-factura.dto'';';" ^
    "Add-Content -Path 'factura.service.ts' -Value 'import { UpdateFacturaDto } from ''./dto/update-factura.dto'';';" ^
    "Add-Content -Path 'factura.service.ts' -Value 'import { Factura } from ''./entities/factura.entity'';';" ^
    "Add-Content -Path 'factura.service.ts' -Value 'import { InjectRepository } from ''@nestjs/typeorm'';';" ^
    "Add-Content -Path 'factura.service.ts' -Value '@Injectable()';" ^
    "Add-Content -Path 'factura.service.ts' -Value 'export class FacturaService {';" ^
    "Add-Content -Path 'factura.service.ts' -Value 'constructor(@InjectRepository(Factura)private facturaRepo: Repository<Factura>,){ }';" ^
    "Add-Content -Path 'factura.service.ts' -Value ' async create(data: CreateFacturaDto){';" ^
    "Add-Content -Path 'factura.service.ts' -Value '     try{';" ^
    "Add-Content -Path 'factura.service.ts' -Value '         const newObject = this.facturaRepo.create(data);';" ^
    "Add-Content -Path 'factura.service.ts' -Value '         return {';" ^
    "Add-Content -Path 'factura.service.ts' -Value '             statusCode: 201,';" ^
    "Add-Content -Path 'factura.service.ts' -Value '             message: ''Create'',';" ^
    "Add-Content -Path 'factura.service.ts' -Value '             response: await this.facturaRepo.save(newObject)';" ^
    "Add-Content -Path 'factura.service.ts' -Value '             }';" ^
    "Add-Content -Path 'factura.service.ts' -Value '     }catch(error) {';" ^
    "Add-Content -Path 'factura.service.ts' -Value '         return {';" ^
    "Add-Content -Path 'factura.service.ts' -Value '             statusCode: 500,';" ^
    "Add-Content -Path 'factura.service.ts' -Value '             message: ''Error Interno'' ';" ^
    "Add-Content -Path 'factura.service.ts' -Value '             }';" ^
    "Add-Content -Path 'factura.service.ts' -Value '     }';" ^
    "Add-Content -Path 'factura.service.ts' -Value ' }';" ^
    "Add-Content -Path 'factura.service.ts' -Value ' async findAll(){ return await this.facturaRepo.find({relations: [''fk_cliente_factura'',] });}';" ^
    "Add-Content -Path 'factura.service.ts' -Value ' async findOne(id_factura: number){ return await this.facturaRepo.find({where:{ id_factura: id_factura}, relations: [''fk_cliente_factura'',] });}';" ^
    "Add-Content -Path 'factura.service.ts' -Value ' async update(id_factura: number, data: UpdateFacturaDto){';" ^
    "Add-Content -Path 'factura.service.ts' -Value '     try{';" ^
    "Add-Content -Path 'factura.service.ts' -Value '         const upd = await this.facturaRepo.findOne({where:{ id_factura: id_factura} });';" ^
    "Add-Content -Path 'factura.service.ts' -Value '         if(upd){';" ^
    "Add-Content -Path 'factura.service.ts' -Value '             await this.facturaRepo.merge(upd, data);';" ^
    "Add-Content -Path 'factura.service.ts' -Value '             return {';" ^
    "Add-Content -Path 'factura.service.ts' -Value '                 statusCode: 201,';" ^
    "Add-Content -Path 'factura.service.ts' -Value '                 message: ''Update'',';" ^
    "Add-Content -Path 'factura.service.ts' -Value '                 response: await this.facturaRepo.save(upd)';" ^
    "Add-Content -Path 'factura.service.ts' -Value '             }';" ^
    "Add-Content -Path 'factura.service.ts' -Value '          }else{';" ^
    "Add-Content -Path 'factura.service.ts' -Value '             return {';" ^
    "Add-Content -Path 'factura.service.ts' -Value '                 statusCode: 200,';" ^
    "Add-Content -Path 'factura.service.ts' -Value '                 message: ''Usuario no encontrado'' ';" ^
    "Add-Content -Path 'factura.service.ts' -Value '                 }';" ^
    "Add-Content -Path 'factura.service.ts' -Value '           }';" ^
    "Add-Content -Path 'factura.service.ts' -Value '      }catch(error) { return { statusCode: 500, message: ''Error Interno''} }';" ^
    "Add-Content -Path 'factura.service.ts' -Value ' }';" ^
    "Add-Content -Path 'factura.service.ts' -Value ' async remove(id_factura: number){';" ^
    "Add-Content -Path 'factura.service.ts' -Value '     try{';" ^
    "Add-Content -Path 'factura.service.ts' -Value '         const dlt = await this.facturaRepo.findOne({where:{ id_factura: id_factura} });';" ^
    "Add-Content -Path 'factura.service.ts' -Value '         if(dlt){';" ^
    "Add-Content -Path 'factura.service.ts' -Value '             await this.facturaRepo.delete(dlt);';" ^
    "Add-Content -Path 'factura.service.ts' -Value '             return {';" ^
    "Add-Content -Path 'factura.service.ts' -Value '                 statusCode: 200,';" ^
    "Add-Content -Path 'factura.service.ts' -Value '                 message: ''Delete'',';" ^
    "Add-Content -Path 'factura.service.ts' -Value '             }';" ^
    "Add-Content -Path 'factura.service.ts' -Value '          }else{';" ^
    "Add-Content -Path 'factura.service.ts' -Value '             return {';" ^
    "Add-Content -Path 'factura.service.ts' -Value '                 statusCode: 200,';" ^
    "Add-Content -Path 'factura.service.ts' -Value '                 message: ''Usuario no encontrado'' ';" ^
    "Add-Content -Path 'factura.service.ts' -Value '                 }';" ^
    "Add-Content -Path 'factura.service.ts' -Value '           }';" ^
    "Add-Content -Path 'factura.service.ts' -Value '      }catch(error) { return { statusCode: 500, message: ''Error Interno''} }';" ^
    "Add-Content -Path 'factura.service.ts' -Value ' }';" ^
    "Add-Content -Path 'factura.service.ts' -Value '}';" ^

cd ..
cd ..
cd factura
@echo off
powershell -Command ^
    "Set-Content -Path 'factura.module.ts' -Value $null;" ^
    "Add-Content -Path 'factura.module.ts' -Value 'import { Module } from ''@nestjs/common'';';" ^
    "Add-Content -Path 'factura.module.ts' -Value 'import { TypeOrmModule } from ''@nestjs/typeorm'';';" ^
    "Add-Content -Path 'factura.module.ts' -Value 'import { FacturaService } from ''./factura.service'';';" ^
    "Add-Content -Path 'factura.module.ts' -Value 'import { FacturaController } from ''./factura.controller'';';" ^
    "Add-Content -Path 'factura.module.ts' -Value 'import { Factura } from ''./entities/factura.entity'';';" ^
    "Add-Content -Path 'factura.module.ts' -Value '@Module({';" ^
    "Add-Content -Path 'factura.module.ts' -Value '  imports: [TypeOrmModule.forFeature([Factura])],';" ^
    "Add-Content -Path 'factura.module.ts' -Value '  controllers: [FacturaController],';" ^
    "Add-Content -Path 'factura.module.ts' -Value '  providers: [FacturaService],';" ^
    "Add-Content -Path 'factura.module.ts' -Value '  exports: [FacturaService],';" ^
    "Add-Content -Path 'factura.module.ts' -Value '})';" ^
    "Add-Content -Path 'factura.module.ts' -Value 'export class FacturaModule { }';" ^

cd ..
cd ..
cd ..
powershell -Command "Start-Process cmd -ArgumentList '/c npm i @nestjs/typeorm typeorm sqlite3' -NoNewWindow -Wait"
echo .
rem Crear la base de datos con un script de Python incluido en el archivo .bat
echo Creando la base de datos SQLite...
echo .
cd src
@echo off
powershell -Command ^
    "Set-Content -Path 'app.module.ts' -Value $null;" ^
    "Add-Content -Path 'app.module.ts' -Value 'import { Module } from ''@nestjs/common'';';" ^
    "Add-Content -Path 'app.module.ts' -Value 'import { AppController } from ''./app.controller'';';" ^
    "Add-Content -Path 'app.module.ts' -Value 'import { AppService } from ''./app.service'';';" ^
    "Add-Content -Path 'app.module.ts' -Value 'import { TypeOrmModule } from ''@nestjs/typeorm'';';" ^
    "Add-Content -Path 'app.module.ts' -Value 'import { ClienteModule } from ''./cliente/cliente.module'';';" ^
    "Add-Content -Path 'app.module.ts' -Value 'import { Cliente } from ''./cliente/entities/cliente.entity'';';" ^
    "Add-Content -Path 'app.module.ts' -Value 'import { FacturaModule } from ''./factura/factura.module'';';" ^
    "Add-Content -Path 'app.module.ts' -Value 'import { Factura } from ''./factura/entities/factura.entity'';';" ^
    "Add-Content -Path 'app.module.ts' -Value '@Module({';" ^
    "Add-Content -Path 'app.module.ts' -Value 'imports: [TypeOrmModule.forRoot({type: ''sqlite'', database: ''database.sqlite'',entities: [Cliente,Factura,], synchronize: true, }), TypeOrmModule.forFeature([Cliente,Factura,]), ClienteModule,FacturaModule,],';" ^
    "Add-Content -Path 'app.module.ts' -Value 'controllers: [AppController],';" ^
    "Add-Content -Path 'app.module.ts' -Value 'providers: [AppService],';" ^
    "Add-Content -Path 'app.module.ts' -Value '})';" ^
    "Add-Content -Path 'app.module.ts' -Value 'export class AppModule { }';" ^
cd ..
powershell -Command "Start-Process cmd -ArgumentList '/c npm i class-validator' -NoNewWindow -Wait"
echo .
powershell -Command "Start-Process cmd -ArgumentList '/c npm i class-transformer' -NoNewWindow -Wait"
echo .
powershell -Command "Start-Process cmd -ArgumentList '/c npm i @nestjs/mapped-types' -NoNewWindow -Wait"
echo .
powershell -Command "Start-Process cmd -ArgumentList '/c npm run start:dev' -NoNewWindow -Wait"
echo .
pause