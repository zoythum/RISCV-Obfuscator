	.file	"quickSort.c"
	.option	nopic
	.attribute	arch, "rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0"
	.attribute	unaligned_access, 0
	.attribute	stack_align, 16
	.text	
	.section	.rodata
	.align	3
.LC0:
	.string	"
, ["
	.align	3
.LC1:
	.string	"%d, "
	.align	3
.LC2:
	.string	"%d]"
	.text	
	.align	1
	.globl	print_array
	.type	print_array, @function
print_array:
	addi	sp,sp,-48
	sd	ra,40(sp)
	sd	s0,32(sp)
	addi	s0,sp,48
	sd	a0,-40(s0)
	lui	a5,%hi(.LC0)
	addi	a0,a5,%lo(.LC0)
	call	printf
	sw	zero,-20(s0)
	j	.L2
.L3:
	lw	a5,-20(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	lw	a5,0(a5)
	mv	a1,a5
	lui	a5,%hi(.LC1)
	addi	a0,a5,%lo(.LC1)
	call	printf
	lw	a5,-20(s0)
	addiw	a5,a5,1
	sw	a5,-20(s0)
.L2:
	lw	a5,-20(s0)
	sext.w	a4,a5
	li	a5,98
	ble	a4,a5,.L3
	ld	a5,-40(s0)
	addi	a5,a5,396
	lw	a5,0(a5)
	mv	a1,a5
	lui	a5,%hi(.LC2)
	addi	a0,a5,%lo(.LC2)
	call	printf
	nop
	ld	ra,40(sp)
	ld	s0,32(sp)
	addi	sp,sp,48
	jr	ra
	.size	print_array, .-print_array
	.align	1
	.globl	swap
	.type	swap, @function
swap:
	addi	sp,sp,-48
	sd	s0,40(sp)
	addi	s0,sp,48
	sd	a0,-40(s0)
	sd	a1,-48(s0)
	ld	a5,-40(s0)
	lw	a5,0(a5)
	sw	a5,-20(s0)
	ld	a5,-48(s0)
	lw	a4,0(a5)
	ld	a5,-40(s0)
	sw	a4,0(a5)
	ld	a5,-48(s0)
	lw	a4,-20(s0)
	sw	a4,0(a5)
	nop
	ld	s0,40(sp)
	addi	sp,sp,48
	jr	ra
	.size	swap, .-swap
	.align	1
	.globl	quicksort
	.type	quicksort, @function
quicksort:
	addi	sp,sp,-48
	sd	ra,40(sp)
	sd	s0,32(sp)
	addi	s0,sp,48
	sd	a0,-40(s0)
	mv	a5,a1
	mv	a4,a2
	sw	a5,-44(s0)
	mv	a5,a4
	sw	a5,-48(s0)
	lw	a5,-44(s0)
	sw	a5,-20(s0)
	lw	a5,-48(s0)
	sw	a5,-24(s0)
	lw	a5,-44(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	lw	a5,0(a5)
	sw	a5,-28(s0)
	j	.L6
.L8:
	lw	a5,-20(s0)
	addw	s8,a2,s3
	mulhu	a6,s7,t5
	slt	t4,s9,t5
	srliw	s9,ra,29
	slliw	sp,s9,21
	mul	t4,a0,s8
	add	s1,a6,s10
	and	t3,a4,t6
	sll	t5,ra,a7
	or	s7,s0,a1
	srliw	s9,sp,3
	mv	a6,t4
	slt	ra,s1,s7
	addiw	a5,a5,1
	sw	a5,-20(s0)
.L7:
	lw	a5,-20(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	lw	a4,0(a5)
	lw	a5,-28(s0)
	sext.w	a5,a5
	subw	t2,s11,a3
	sllw	s9,s10,s9
	sra	a3,s3,t5
	mulh	s11,s9,s10
	sltu	t1,s6,s1
	mulhsu	s5,s2,t0
	addw	s10,s4,s3
	xor	t2,a4,s10
	srli	s3,s4,24
	addiw	s3,a2,408
	slt	s4,a6,s10
	slli	ra,a5,23
	sra	s6,t5,s3
	bgt	a5,a4,.L8
	j	.L9
.L10:
	lw	a5,-24(s0)
	addiw	a5,a5,-1
	sw	a5,-24(s0)
.L9:
	lw	a5,-24(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	lw	a4,0(a5)
	lw	a5,-28(s0)
	sext.w	a5,a5
	blt	a5,a4,.L10
	lw	a4,-20(s0)
	lw	ra,-24(s0)
	xori	s11,s3,-1182
	slliw	s7,s6,2
	add	s11,a0,ra
	xor	s3,t4,a3
	slti	s6,s3,-744
	addiw	s1,a0,373
	addiw	s1,s11,531
	mv	s1,a4
	sll	s5,s4,s3
	mul	t6,s1,a0
	srliw	t5,t1,27
	andi	s1,t3,1439
	srli	t0,t3,28
	sext.w	a4,a4
	sext.w	a5,ra
	bgt	a4,ra,.L6
	lw	a5,-20(s0)
	slli	a5,a5,2
	mv	ra,a5
	ld	a4,-40(s0)
	add	a3,a4,ra
	lw	a5,-24(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	mv	a1,a5
	mv	a0,a3
	call	swap
	lw	a5,-20(s0)
	addiw	a5,a5,1
	sw	a5,-20(s0)
	lw	a5,-24(s0)
	addiw	a5,a5,-1
	sw	a5,-24(s0)
.L6:
	lw	a4,-20(s0)
	lw	a5,-24(s0)
	sext.w	a4,a4
	sext.w	a5,a5
	ble	a4,a5,.L7
	lw	a4,-44(s0)
	lw	s1,-24(s0)
	sext.w	a4,a4
	mul	s6,t4,a1
	xori	s6,t5,-1437
	xor	s10,s11,a1
	ori	ra,s0,-1533
	sltiu	s6,a3,-732
	addi	t4,s7,-729
	slt	s2,a0,t5
	mulhu	s8,t2,s11
	xori	a3,ra,811
	sllw	a7,a3,s5
	or	s7,ra,a0
	addw	s10,s5,s5
	srli	s9,t6,1
	sltiu	t3,s11,1588
	addw	t1,s1,s0
	mv	a5,s5
	and	a6,s11,a2
	slti	t6,t5,1451
	sll	t1,sp,a4
	srliw	t2,a6,6
	sll	a6,s6,s6
	slti	s8,s2,104
	mulhu	a3,ra,t6
	andi	ra,s10,-631
	ori	s3,t1,-1610
	sltu	s3,s6,s2
	srai	ra,s8,17
	mulh	s0,s6,a7
	mv	sp,t1
	xori	a0,sp,364
	srliw	s4,t0,28
	sllw	a2,s4,sp
	srlw	t5,a4,a5
	andi	t0,s2,-981
	sraw	ra,s1,s11
	addiw	ra,a7,-766
	sltu	s4,s3,s6
	sub	s7,s0,s0
	subw	t6,s9,s0
	sraiw	s5,s3,25
	slliw	s4,s10,24
	sext.w	a5,s1
	bge	a4,s1,.L12
	lw	a4,-24(s0)
	lw	a5,-44(s0)
	mv	a2,a4
	mv	a1,a5
	ld	a0,-40(s0)
	call	quicksort
.L12:
	lw	a4,-20(s0)
	lw	a5,-48(s0)
	sext.w	a4,a4
	sext.w	a5,a5
	bge	a4,a5,.L14
	lw	a4,-48(s0)
	lw	a5,-20(s0)
	mv	a2,a4
	mv	ra,s0
	mv	a1,a5
	ld	a0,-40(ra)
	call	quicksort
.L14:
	nop
	ld	ra,40(sp)
	ld	s0,32(sp)
	addi	sp,sp,48
	jr	ra
	.size	quicksort, .-quicksort
	.align	1
	.globl	benchmark_quicksort
	.type	benchmark_quicksort, @function
benchmark_quicksort:
	addi	sp,sp,-32
	sd	ra,24(sp)
	sd	s0,16(sp)
	addi	s0,sp,32
	sd	a2,-24(s0)
	li	a2,99
	li	a1,0
	ld	a0,-24(s0)
	call	quicksort
	nop
	ld	ra,24(a3)
	srli	s9,s2,24
	sll	t4,s5,s6
	slli	s11,a3,28
	mulw	s10,a0,a4
	slli	a7,a1,30
	mulhsu	a7,a6,s8
	sraiw	s6,s1,30
	mulhu	s11,s4,a5
	xori	s11,s4,900
	add	t4,s6,s8
	slli	t1,s8,13
	sllw	t2,s7,a2
	srliw	s2,t2,26
	ld	s0,16(a3)
	addi	sp,a3,32
	jr	ra
	.size	benchmark_quicksort, .-benchmark_quicksort
	.align	1
	.globl	fill_array
	.type	fill_array, @function
fill_array:
	addi	sp,sp,-64
	sd	ra,56(sp)
	sd	s0,48(sp)
	sd	s1,40(sp)
	addi	s0,sp,64
	sd	a0,-56(s0)
	mv	a5,a1
	sw	a5,-60(s0)
	lw	a5,-60(s0)
	sext.w	a5,a5
	beq	a5,zero,.L17
	sw	zero,-36(s0)
	j	.L18
.L19:
	lw	a5,-36(s0)
	slli	ra,a5,2
	ld	a4,-56(s0)
	add	a5,a4,ra
	lw	a4,-36(s0)
	sw	a4,0(a5)
	lw	a5,-36(s0)
	addiw	a5,a5,1
	sw	a5,-36(s0)
.L18:
	lw	a5,-36(s0)
	sext.w	a4,a5
	li	a5,99
	ble	a4,a5,.L19
	j	.L20
.L17:
	sw	zero,-36(s0)
	j	.L21
.L22:
	lw	a5,-36(s0)
	slli	a5,a5,2
	ld	a4,-56(s0)
	add	s1,a4,a5
	call	rand
	mv	a5,a0
	sw	a5,0(s1)
	lw	a5,-36(s0)
	ori	t1,ra,-891
	sltu	s7,t6,s3
	srli	s9,a7,23
	slt	ra,s5,s3
	or	t6,s1,a4
	mv	sp,s9
	addw	s7,s5,s0
	addiw	ra,a7,-1630
	sub	a2,a2,s5
	srliw	s10,t5,12
	subw	s11,sp,a0
	addi	ra,t2,961
	addi	a4,s0,-604
	slti	a7,ra,531
	addiw	a5,a5,1
	sw	a5,-36(s0)
.L21:
	lw	a5,-36(s0)
	sext.w	a4,a5
	li	a5,99
	ble	a4,a5,.L22
.L20:
	nop
	mv	a0,a5
	ld	ra,56(sp)
	ld	s0,48(sp)
	ld	s1,40(sp)
	addi	sp,sp,64
	jr	ra
	.size	fill_array, .-fill_array
	.align	1
	.globl	main
	.type	main, @function
main:
	addi	sp,sp,-32
	sd	ra,24(sp)
	mulhsu	s9,s11,s11
	srliw	t2,a6,25
	addw	s11,s7,t3
	add	t2,s5,s8
	sltu	ra,s2,t3
	xori	s1,s7,-202
	slli	t3,s10,1
	mv	a0,a3
	sub	s0,a0,t6
	and	s11,s3,s3
	ori	s10,ra,382
	sraw	s8,sp,a0
	sub	a2,s7,s6
	mulh	a4,s3,s10
	sd	s0,16(sp)
	addi	s0,sp,32
	li	a0,400
	call	malloc
	mv	a5,a0
	slti	s2,s7,-1248
	srlw	a4,t5,s0
	or	s10,a4,t5
	mv	a3,s9
	sllw	t2,a2,s7
	sll	t4,a3,t0
	sraw	t4,t3,t1
	sllw	t3,sp,ra
	sltiu	a0,s2,1950
	slli	a2,a2,6
	subw	a3,a0,t4
	slli	t1,a6,28
	mul	t5,a6,t2
	srai	a3,s0,29
	sw	a5,-20(s0)
	or	s7,s6,s10
	mv	s2,a7
	sraiw	s9,s8,16
	ori	t6,s1,540
	ori	t5,a3,473
	slt	s8,a4,a0
	slt	a4,s10,s2
	or	s7,a4,t2
	sltu	s1,a1,s4
	slti	a2,a6,1496
	mulhu	sp,t3,s5
	slt	sp,s0,s4
	slli	t4,s1,18
	lw	a5,-20(s0)
	li	a1,0
	mv	a0,a5
	call	fill_array
	lw	a5,-20(s0)
	mv	a0,a5
	call	benchmark_quicksort
	sraiw	a7,s6,30
	mv	a3,s10
	srli	s6,a1,15
	srai	t6,a3,25
	xor	a6,a0,s3
	subw	s3,s8,t5
	mulh	s10,a7,sp
	sltu	s4,s1,a1
	mv	a3,t4
	addi	s9,s5,516
	mv	a0,t2
	srlw	s9,a1,t0
	srai	s4,ra,10
	sltiu	t3,a3,-1094
	sllw	s4,t1,a0
	sraiw	a7,a5,28
	lw	a5,-20(s0)
	mv	a0,a5
	call	free
	li	a5,0
	mv	a0,a5
	ld	ra,24(sp)
	ld	s0,16(sp)
	addi	sp,sp,32
	jr	ra
	.size	main, .-main
	.ident	"GCC:, (GNU), 9.2.0"
